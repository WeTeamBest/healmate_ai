# HealMate AI — Emotion Detection & Healing Score

## 📋 Deskripsi Proyek

Proyek ini membangun sistem deteksi emosi berbasis deep learning untuk aplikasi **HealMate** — platform digital yang mendampingi pengguna yang sedang pulih dari putus cinta. Model memprediksi emosi pengguna dari teks (anxiety, anger, acceptance) sekaligus menghasilkan **healing score** yang mencerminkan tingkat pemulihan emosional mereka.

Hasil prediksi digunakan untuk menghasilkan respons konselor empatik dan saran aktivitas yang dipersonalisasi melalui integrasi **Gemini AI**.

### Tujuan Proyek

- Mendeteksi emosi pengguna (anxiety, anger, acceptance) dari teks berbahasa Indonesia maupun Inggris
- Memprediksi healing score sebagai representasi numerik tingkat pemulihan emosional
- Membandingkan performa 6 arsitektur deep learning (LSTM, GRU, CNN, BiLSTM, BiGRU, BERT)
- Mengekspor model terbaik sebagai SavedModel untuk digunakan di REST API produksi
- Mengintegrasikan prediksi model dengan Gemini AI untuk respons konselor yang kontekstual

### Dataset

Data yang digunakan adalah **Emotion Dataset Merged** yang sudah melalui proses labeling emosi sebelumnya:

- **Kolom utama**: `input_clean` (teks), `predicted_emotion` (label emosi), `emotion_confidence`, `acceptance_prob`, `anger_prob`, `anxiety_prob`
- **Kelas emosi**: anxiety, anger, acceptance
- **Healing score**: diturunkan dari probabilitas emosi → `acceptance_prob − (anger_prob + anxiety_prob) / 2`

---

## 🏗️ Struktur Proyek

```
healmate_ai/
│
├── AI/
│   ├── dataset/
│   │   └── Emotion Dataset Merged.xlsx     # Dataset utama
│   │
│   ├── inference/
│   │   └── inference.ipynb                 # Testing & prediksi model
│   │
│   ├── Main/
│   │   ├── notebook.ipynb                  # EDA, training, evaluasi
│   │   └── results/
│   │       ├── artifacts/
│   │       │   ├── tokenizer.pkl           # Tokenizer hasil training
│   │       │   ├── label_encoder.pkl       # Label encoder kelas emosi
│   │       │   └── eval_results.json       # Hasil evaluasi semua model
│   │       ├── best_model/                 # SavedModel format (model terbaik)
│   │       ├── all_models/                 # SavedModel semua arsitektur
│   │       └── logs/                       # TensorBoard logs
│   │
│   └── REST API/
│       ├── main.py                         # FastAPI entrypoint
│       ├── predictor.py                    # Logika prediksi + Gemini
│       ├── preprocessing_noprob.py         # Fungsi preprocessing teks
│       ├── .env                            # API Key (tidak di-push)
│       └── .env-example                    # Template environment variables
```

---

## 📊 Pipeline Proyek

```
┌──────────────────────────────────────────────────────────────┐
│ 1. EDA & PREPROCESSING (notebook.ipynb)                     │
│    - Load Emotion Dataset Merged.xlsx                        │
│    - Analisis distribusi kelas & panjang teks                │
│    - Hitung healing score dari probabilitas emosi            │
│    - Split data → Train 80% / Val 10% / Test 10%            │
└───────────────────────┬──────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. TOKENISASI & DATASET (notebook.ipynb)                    │
│    - Tokenizer Keras (num_words=10.000, max_length=200)      │
│    - Padding & truncation                                    │
│    - tf.data.Dataset dengan shuffle, batch, prefetch         │
│    - Class weight balancing                                  │
└───────────────────────┬──────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. MODELING & TRAINING (notebook.ipynb)                     │
│    - 6 arsitektur: LSTM, GRU, CNN, BiLSTM, BiGRU, BERT      │
│    - Custom Embedding & Dense Layer                          │
│    - Multi-output: klasifikasi emosi + regresi healing score │
│    - TensorBoard logging per model                           │
└───────────────────────┬──────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. EVALUASI & SIMPAN MODEL (notebook.ipynb)                 │
│    - Evaluasi: accuracy, F1 macro, F1 weighted, MAE healing  │
│    - Pilih model terbaik otomatis berdasarkan F1 macro       │
│    - Simpan semua model (.keras + SavedModel)                │
│    - Ekspor best_model → SavedModel untuk REST API           │
└───────────────────────┬──────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│ 5. INFERENCE (inference.ipynb + REST API)                   │
│    - Load SavedModel best_model                              │
│    - Prediksi emosi + healing score dari teks baru           │
│    - Integrasi Gemini AI → respons konselor + saran aktivitas│
│    - REST API via FastAPI                                    │
└──────────────────────────────────────────────────────────────┘
```

---

## 📝 Deskripsi File

### 1. **notebook.ipynb**

**Tujuan**: EDA, preprocessing, training semua model, evaluasi, dan penyimpanan

**Tahapan Utama**:

#### A. **Load Dataset & EDA**

- Membaca `Emotion Dataset Merged.xlsx`
- Analisis distribusi kelas emosi (bar chart + pie chart)
- Pemeriksaan missing values, duplikat, dan noise (confidence < 0.5)
- Statistik panjang teks

#### B. **Feature Engineering**

- Menghitung healing score dari probabilitas emosi:
  ```
  healing_score = acceptance_prob − (anger_prob + anxiety_prob) / 2
  ```
- Label encoding kelas emosi
- Split stratified: Train 80% / Val 10% / Test 10%

#### C. **Tokenisasi & Padding**

- Keras Tokenizer dengan `num_words=10.000`, `oov_token='<OOV>'`
- Padding & truncation dengan `max_length=200`
- tf.data.Dataset pipeline (shuffle, batch=32, prefetch)
- Class weight balancing untuk menangani imbalance

#### D. **Custom Layers**

- `CustomEmbeddingLayer`: embedding dengan masking token padding
- `CustomDenseLayer`: dense dengan dropout terintegrasi

#### E. **Model Training**

Semua model menggunakan arsitektur **multi-output**:
- Output 1: klasifikasi emosi (softmax, 3 kelas)
- Output 2: regresi healing score (sigmoid/linear, 1 nilai)

| Model  | Arsitektur Utama                        |
|--------|-----------------------------------------|
| LSTM   | Embedding → LSTM → Dense               |
| GRU    | Embedding → GRU → Dense                |
| CNN    | Embedding → Conv1D → GlobalMaxPool → Dense |
| BiLSTM | Embedding → Bidirectional LSTM → Dense |
| BiGRU  | Embedding → Bidirectional GRU → Dense  |
| BERT   | IndoBERT → Custom Head → Dense         |

#### F. **Evaluasi & Pemilihan Model Terbaik**

- Metrik: accuracy, F1 macro, F1 weighted, MAE healing score
- Target: accuracy ≥ 0.85, F1 macro ≥ 0.85, MAE healing ≤ 0.2
- Model terbaik dipilih otomatis berdasarkan F1 macro tertinggi
- Visualisasi perbandingan 4 metrik antar semua model

#### G. **Penyimpanan Model**

- Semua model → `.keras` dan SavedModel format
- Model terbaik → `results/best_model/` (SavedModel, untuk REST API)
- Artifacts → `tokenizer.pkl`, `label_encoder.pkl`, `eval_results.json`

---

### 2. **inference.ipynb**

**Tujuan**: Testing model terbaik dengan teks baru, termasuk integrasi Gemini AI

**Tahapan**:

#### A. **Setup & Load Artifacts**

- Load tokenizer dan label encoder dari `results/artifacts/`
- Load SavedModel terbaik dari `results/best_model/`
- Load API Key Gemini dari `REST API/.env`

#### B. **Fungsi Prediksi**

```python
predict(text) → dict
```

Alur prediksi:
1. Terjemahkan teks ke Bahasa Inggris (Google Translate)
2. Preprocessing teks (`clean_text`)
3. Tokenisasi + padding → tensor
4. Inferensi model → deteksi output emotion vs healing secara otomatis dari shape
5. Panggil Gemini untuk respons konselor + saran aktivitas

#### C. **Output Prediksi**

```python
{
    "text_original"        : teks asli,
    "text_english"         : teks setelah diterjemahkan,
    "text_clean"           : teks setelah preprocessing,
    "emotion"              : label emosi (anxiety/anger/acceptance),
    "confidence"           : confidence score,
    "all_emotions"         : distribusi probabilitas semua kelas,
    "healing_score"        : nilai healing (-1.0 s/d 1.0),
    "counselor_response"   : respons konselor dari Gemini,
    "activity_suggestions" : 5 saran aktivitas dari Gemini,
}
```

#### D. **Test Sentences**

```python
test_sentences = [
    "Aku masih nggak bisa ngerti kenapa dia pergi tanpa alasan yang jelas",
    "I feel so angry, he betrayed my trust completely",
    "Slowly I'm starting to accept things and move on",
    "I don't know what to feel anymore, everything is numb",
]
```

---

### 3. **REST API** (`main.py` + `predictor.py`)

**Tujuan**: Menyajikan prediksi sebagai HTTP endpoint

**Endpoint**:

| Method | Path       | Deskripsi                        |
|--------|------------|----------------------------------|
| GET    | `/`        | Health check API                 |
| POST   | `/predict` | Prediksi emosi + healing score   |

**Request**:
```json
{ "text": "Aku masih nggak bisa ngerti kenapa dia pergi" }
```

**Response**:
```json
{
  "emotion": "anxiety",
  "confidence": 0.8921,
  "healing_score": -0.1243,
  "counselor_response": "...",
  "activity_suggestions": ["...", "...", "...", "...", "..."]
}
```

---

### 4. **preprocessing_noprob.py**

Modul preprocessing teks yang dipakai bersama oleh notebook dan REST API:

- `clean_text(text)`: lowercase → hapus URL → expand contractions → hapus tanda baca → hapus non-huruf → rapikan spasi
- `expand_contractions(text)`: menjabarkan singkatan Inggris informal (contoh: `"dont"` → `"do not"`)
- Dictionary contractions mencakup 100+ pola formal dan informal

---

## 🛠️ Instalasi & Setup

### Prerequisites

- Python 3.9+
- pip

### 1. Clone Repository

```bash
git clone https://github.com/WeTeamBest/healmate_ai.git
cd healmate_ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp "AI/REST API/.env-example" "AI/REST API/.env"
```

Isi file `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 📦 Dependencies Utama

```
tensorflow          # Deep learning framework
transformers        # BERT (IndoBERT)
scikit-learn        # LabelEncoder, metrics
pandas / numpy      # Data manipulation
matplotlib / seaborn # Visualisasi
deep-translator     # Google Translate (inference)
google-generativeai # Gemini AI integration
fastapi / uvicorn   # REST API
python-dotenv       # Environment variables
```

---

## 🚀 Cara Menggunakan

### Skenario 1: Training dari Awal

1. **Siapkan dataset** di `AI/dataset/Emotion Dataset Merged.xlsx`
2. **Jalankan training** (`AI/Main/notebook.ipynb`)
   - Run semua cells secara berurutan
   - Output: model tersimpan di `AI/Main/results/`
3. **Jalankan inference notebook** (`AI/inference/inference.ipynb`)
   - Pastikan `.env` sudah dikonfigurasi
   - Run semua cells untuk test prediksi

### Skenario 2: Menggunakan Model Terlatih (Hanya Inference)

1. Pastikan folder `AI/Main/results/best_model/` dan `AI/Main/results/artifacts/` sudah ada
2. Buka `AI/inference/inference.ipynb`
3. Run semua cells

### Skenario 3: Menjalankan REST API

```bash
cd "AI/REST API"
uvicorn main:app --reload
```

API tersedia di `http://localhost:8000`. Dokumentasi otomatis di `http://localhost:8000/docs`.

---

## 📈 Model & Performa

### Arsitektur Model

Semua model menggunakan pendekatan **multi-task learning** dengan dua output:
- **Output emosi**: klasifikasi 3 kelas (softmax)
- **Output healing**: regresi skor pemulihan (1 nilai)

### Target Performa

| Metrik         | Target   |
|----------------|----------|
| Accuracy       | ≥ 0.85   |
| F1 Macro       | ≥ 0.85   |
| F1 Weighted    | ≥ 0.85   |
| MAE Healing    | ≤ 0.20   |

### Hyperparameter Global

| Parameter    | Nilai  |
|--------------|--------|
| NUM_WORDS    | 10.000 |
| MAX_LENGTH   | 200    |
| EMBED_DIM    | 128    |
| EPOCH        | 50     |
| BATCH_SIZE   | 32     |
| RANDOM_SEED  | 42     |

---

## 🎯 Key Features

✅ **Multi-task Learning**: Prediksi emosi + healing score dalam satu forward pass  
✅ **6 Arsitektur**: LSTM, GRU, CNN, BiLSTM, BiGRU, BERT — perbandingan komprehensif  
✅ **Auto Best Model**: Model terbaik dipilih otomatis berdasarkan F1 macro  
✅ **Multilingual Input**: Input Bahasa Indonesia otomatis diterjemahkan ke Inggris  
✅ **Gemini Integration**: Respons konselor & saran aktivitas yang dipersonalisasi  
✅ **SavedModel Export**: Model diekspor ke format SavedModel untuk produksi  
✅ **REST API**: FastAPI endpoint siap deploy  
✅ **TensorBoard**: Logging training semua model  

---

## 🔧 Troubleshooting

### GEMINI_API_KEY tidak terbaca

Pastikan path `.env` benar. Inference notebook membaca dari:
```
AI/REST API/.env
```
Bukan dari folder notebook itu sendiri.

### Model output tidak teridentifikasi

Fungsi `predict()` mendeteksi output secara otomatis berdasarkan shape tensor:
- Shape `[batch, n_classes]` → output emosi
- Shape `[batch, 1]` → output healing score

Jika error, cek jumlah kelas di label encoder sesuai dengan output model.

### Memory error saat training BERT

- Kurangi `BATCH_SIZE` (coba 16 atau 8)
- Pastikan GPU VRAM mencukupi (minimal 8GB untuk BERT)
- Gunakan `tf.keras.mixed_precision` untuk efisiensi memori

### Module `preprocessing_noprob` tidak ditemukan

Inference notebook mencari modul ini di folder `REST API/`. Pastikan `sys.path` sudah mengarah ke folder tersebut — sudah ditangani otomatis di Cell 1 inference notebook.

---

## 👨‍💻 Author & Project Info

**Author**: Ahmad Farizky  
**Project**: HealMate AI — Emotion Detection & Healing Score  
**Institution**: Capstone Project  
**Date**: 2026

---

**Last Updated**: 2026-06-01  
**Version**: 1.0
