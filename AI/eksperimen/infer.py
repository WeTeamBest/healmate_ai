#!/usr/bin/env python3
"""Inference helper for AI/eksperimen models.

This script is built to load the saved PyTorch multi-task emotion model from
`best_model.pt` together with `model_config.json` and `AutoTokenizer`.

Example:
  python AI/eksperimen/infer.py --model AI/eksperimen/best_model.pt --text "Saya sedih"
  python AI/eksperimen/infer.py --model AI/eksperimen/best_model.pt --input_csv data/test.csv --output_csv data/preds.csv
"""

import argparse
import json
import os
import pickle
import sys

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    torch = None
    nn = None
    F = None

try:
    from transformers import AutoModel, AutoTokenizer
except ImportError:
    AutoModel = None
    AutoTokenizer = None

try:
    from tensorflow import keras
except Exception:
    keras = None


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def find_default_config(model_path):
    model_dir = os.path.dirname(os.path.abspath(model_path))
    candidate = os.path.join(model_dir, "model_config.json")
    if os.path.exists(candidate):
        return candidate
    candidate = os.path.join(os.getcwd(), "model_config.json")
    if os.path.exists(candidate):
        return candidate
    return None


def class_name_for_index(index, config, label_encoder=None):
    if label_encoder is not None:
        try:
            return label_encoder.inverse_transform([index])[0]
        except Exception:
            pass
    class_names = config.get("class_names")
    if class_names is not None and len(class_names) > index:
        return class_names[index]
    return str(index)


def zone_from_score(score, config):
    healing_zones = config.get("healing_zones")
    if healing_zones is None:
        if score < 0.3:
            return "TERPURUK"
        if score < 0.7:
            return "TRANSISI"
        return "MENERIMA"
    for zone_name, bounds in healing_zones.items():
        if bounds[0] <= score < bounds[1] or (zone_name == max(healing_zones, key=lambda k: healing_zones[k][1]) and score <= bounds[1]):
            return zone_name.upper()
    return "UNKNOWN"


class MultiTaskEmotionModel(nn.Module):
    def __init__(self, model_name, num_classes, dropout=0.3):
        super(MultiTaskEmotionModel, self).__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        hidden_size = self.bert.config.hidden_size

        self._freeze_bert_layers(freeze_ratio=0.7)

        self.shared_layer = nn.Sequential(
            nn.Linear(hidden_size, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(dropout),
        )

        self.cls_head = nn.Sequential(
            nn.Linear(512, 256),
            nn.LayerNorm(256),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes),
        )

        self.reg_head = nn.Sequential(
            nn.Linear(512, 128),
            nn.LayerNorm(128),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(128, 1),
            nn.Sigmoid(),
        )

    def _freeze_bert_layers(self, freeze_ratio=0.7):
        all_params = list(self.bert.named_parameters())
        freeze_until = int(len(all_params) * freeze_ratio)
        for i, (_, param) in enumerate(all_params):
            if i < freeze_until:
                param.requires_grad = False

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        cls_output = outputs.last_hidden_state[:, 0, :]
        shared = self.shared_layer(cls_output)
        cls_logits = self.cls_head(shared)
        reg_output = self.reg_head(shared).squeeze(-1)
        return cls_logits, reg_output


def load_pytorch_model(model_path, config, device="cpu"):
    if torch is None or AutoModel is None or AutoTokenizer is None:
        raise RuntimeError("PyTorch and transformers are required for this inference path")

    model = MultiTaskEmotionModel(
        model_name=config["model_name"],
        num_classes=config["num_classes"],
        dropout=config.get("dropout", 0.3),
    )
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model


def predict_pytorch(text, model, tokenizer, config, device="cpu", label_encoder=None):
    encoding = tokenizer(
        text,
        max_length=config["max_len"],
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)
    with torch.no_grad():
        cls_logits, healing_score = model(input_ids, attention_mask)

    probs = F.softmax(cls_logits, dim=-1).squeeze(0).cpu().numpy()
    predicted_idx = int(np.argmax(probs))
    predicted_emo = class_name_for_index(predicted_idx, config, label_encoder)
    confidence = float(probs[predicted_idx])
    healing_score = float(healing_score.squeeze(0).cpu().numpy())
    zone = zone_from_score(healing_score, config)
    return {
        "predicted_emotion": predicted_emo,
        "probabilities": {class_name_for_index(i, config, label_encoder): float(probs[i]) for i in range(len(probs))},
        "confidence": confidence,
        "healing_score": healing_score,
        "healing_zone": zone,
    }


def load_keras_model(model_path):
    if keras is None:
        raise RuntimeError("Keras is not installed in this environment")
    return keras.models.load_model(model_path)


def predict_keras(model, x):
    preds = model.predict(x)
    return preds


def format_prediction(result):
    lines = [
        f"Predicted emotion : {result['predicted_emotion']}",
        f"Confidence       : {result['confidence']:.4f}",
        f"Healing score    : {result['healing_score']:.4f}",
        f"Healing zone     : {result['healing_zone']}",
        "Probabilities:" ,
    ]
    for emo, prob in result["probabilities"].items():
        lines.append(f"  {emo:<12}: {prob:.4f}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run inference for the stored emotion model")
    parser.add_argument("--model", required=True, help="Path to the model weights file (.pt or .keras)")
    parser.add_argument("--model-config", help="Path to model_config.json")
    parser.add_argument("--label-encoder", help="Optional path to label_encoder.pkl")
    parser.add_argument("--text", help="Single text input to predict")
    parser.add_argument("--input-csv", help="CSV file with a 'text' column for batch inference")
    parser.add_argument("--output-csv", help="Output CSV file for batch predictions")
    args = parser.parse_args()

    model_path = args.model
    if not os.path.exists(model_path):
        print(f"Model not found: {model_path}")
        sys.exit(1)

    label_encoder = None
    if args.label_encoder:
        if not os.path.exists(args.label_encoder):
            print(f"Label encoder file not found: {args.label_encoder}")
            sys.exit(1)
        label_encoder = load_pickle(args.label_encoder)

    if model_path.lower().endswith(".pt") or model_path.lower().endswith(".pth"):
        config_path = args.model_config or find_default_config(model_path)
        if config_path is None or not os.path.exists(config_path):
            print("Cannot find model_config.json. Please provide --model-config or place model_config.json next to the model.")
            sys.exit(1)
        config = load_json(config_path)
        if AutoTokenizer is None or AutoModel is None or torch is None:
            raise RuntimeError("Please install torch and transformers to run this model")
        tokenizer = AutoTokenizer.from_pretrained(config["model_name"])
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = load_pytorch_model(model_path, config, device=device)

        def infer_text(text):
            return predict_pytorch(text, model, tokenizer, config, device=device, label_encoder=label_encoder)

    elif model_path.lower().endswith(".keras") or model_path.lower().endswith(".h5"):
        if keras is None:
            raise RuntimeError("Please install tensorflow/keras to run this model")
        model = load_keras_model(model_path)

        def infer_text(text):
            x = simple_text_to_sequence(text, maxlen=100)
            preds = predict_keras(model, x)
            return {"predictions": preds.tolist()}

    else:
        print("Unsupported model type. Use .pt/.pth for PyTorch or .keras/.h5 for Keras.")
        sys.exit(1)

    if args.text:
        result = infer_text(args.text)
        print(f"Input: {args.text}")
        print(format_prediction(result) if "predicted_emotion" in result else result)
        return

    if args.input_csv:
        import pandas as pd

        df = pd.read_csv(args.input_csv)
        if "text" not in df.columns:
            print("CSV must contain a 'text' column")
            sys.exit(1)

        results = []
        for text in df["text"].astype(str).tolist():
            result = infer_text(text)
            if "predicted_emotion" in result:
                results.append({
                    "predicted_emotion": result["predicted_emotion"],
                    "confidence": result["confidence"],
                    "healing_score": result["healing_score"],
                    "healing_zone": result["healing_zone"],
                    **{f"prob_{k}": v for k, v in result["probabilities"].items()},
                })
            else:
                results.append({"predictions": result["predictions"]})

        out = args.output_csv or "predictions.csv"
        out_df = pd.concat([df.reset_index(drop=True), pd.DataFrame(results)], axis=1)
        out_df.to_csv(out, index=False)
        print(f"Wrote predictions to {out}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
