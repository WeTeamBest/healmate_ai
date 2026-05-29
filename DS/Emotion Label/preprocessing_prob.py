import re
import numpy as np
import pandas as pd

from collections import Counter


# CONTRACTION DICTIONARY

CONTRACTIONS_DICT = {

    # I
    "i'm": "i am",
    "i've": "i have",
    "i'll": "i will",
    "i'd": "i would",

    "im": "i am",
    "ive": "i have",

    # you
    "you're": "you are",
    "you've": "you have",
    "you'll": "you will",
    "you'd": "you would",

    "youre": "you are",
    "youve": "you have",
    "youll": "you will",
    "youd": "you would",

    # he
    "he's": "he is",
    "he'll": "he will",
    "he'd": "he would",

    "hes": "he is",
    "hed": "he would",

    # she
    "she's": "she is",
    "she'll": "she will",
    "she'd": "she would",

    "shes": "she is",
    "shed": "she would",

    # it
    "it's": "it is",
    "it'll": "it will",
    "it'd": "it would",

    # we
    "we're": "we are",
    "we've": "we have",
    "we'll": "we will",
    "we'd": "we would",

    "weve": "we have",
    "wed": "we would",

    # they
    "they're": "they are",
    "they've": "they have",
    "they'll": "they will",
    "they'd": "they would",

    "theyre": "they are",
    "theyve": "they have",
    "theyll": "they will",
    "theyd": "they would",

    # negation
    "aren't": "are not",
    "isn't": "is not",
    "wasn't": "was not",
    "weren't": "were not",

    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",

    "won't": "will not",
    "wouldn't": "would not",
    "can't": "can not",
    "cannot": "can not",
    "couldn't": "could not",
    "shouldn't": "should not",

    "hadn't": "had not",
    "hasn't": "has not",
    "haven't": "have not",

    "mustn't": "must not",
    "needn't": "need not",

    # typo negation
    "arent": "are not",
    "isnt": "is not",
    "wasnt": "was not",
    "werent": "were not",

    "dont": "do not",
    "doesnt": "does not",
    "didnt": "did not",

    "wont": "will not",
    "wouldnt": "would not",
    "cant": "can not",
    "couldnt": "could not",
    "shouldnt": "should not",

    "hadnt": "had not",
    "hasnt": "has not",
    "havent": "have not",

    # misc
    "that's": "that is",
    "there's": "there is",
    "who's": "who is",
    "what's": "what is",
    "where's": "where is",
    "when's": "when is",
    "why's": "why is",
    "how's": "how is",

    "lets": "let us",
    "let's": "let us",

    "yall": "you all",
    "y'all": "you all",

    # slang
    "gonna": "going to",
    "wanna": "want to",
    "gotta": "got to",
    "kinda": "kind of",
    "sorta": "sort of",
    "dunno": "do not know",

    "ain't": "is not",
    "aint": "is not",

    "tryna": "trying to",
    "hafta": "have to",
    "oughta": "ought to",
}


CONTRACTIONS_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in CONTRACTIONS_DICT.keys()) + r')\b',
    re.IGNORECASE
)

# EMOTION DICTIONARY

anger_words = {

    # HIGH
    "furious": 3,
    "rage": 3,
    "livid": 3,
    "fuming": 3,
    "outrage": 3,
    "hate": 3,
    "loathe": 3,
    "despise": 3,
    "screamed": 3,
    "yelled": 3,
    "betrayed": 3,
    "manipulative": 3,
    "gaslighting": 3,
    "abusive": 3,
    "narcissist": 3,

    # MEDIUM
    "angry": 2,
    "anger": 2,
    "bitter": 2,
    "resentful": 2,
    "frustrated": 2,
    "irritated": 2,
    "disgusted": 2,
    "cruel": 2,
    "heartless": 2,
    "toxic": 2,
    "controlling": 2,
    "lied": 2,
    "cheated": 2,
    "unfaithful": 2,
    "selfish": 2,

    # LOW
    "mad": 1,
    "upset": 1,
    "annoyed": 1,
    "piss": 1,
    "sick": 1,
    "done": 1,
    "fed": 1,
    "trigger": 1,
    "grudge": 1,
    "disappoint": 1,
    "resent": 1,
    "hurt": 1,
    "salty": 1,
    "used": 1,
    "disrespect": 1,
    "humiliate": 1,
    "betray": 1,
    "annoy": 1,
    "frustrate": 1,
    "fury": 1,
    "irritate": 1,
}


anxiety_words = {

    # HIGH
    "terrified": 3,
    "panic": 3,
    "paranoid": 3,
    "desperate": 3,
    "hopeless": 3,
    "obsess": 3,
    "spiral": 3,
    "shattered": 3,
    "helpless": 3,
    "sleepless": 3,
    "dread": 3,

    # MEDIUM
    "anxious": 2,
    "anxiety": 2,
    "afraid": 2,
    "insecure": 2,
    "overthink": 2,
    "overwhelm": 2,
    "lonely": 2,
    "empty": 2,
    "numb": 2,
    "broken": 2,
    "lost": 2,
    "hollow": 2,
    "crying": 2,
    "weeping": 2,
    "tears": 2,
    "clingy": 2,
    "stalk": 2,
    "attachment": 2,

    # LOW
    "worry": 1,
    "nervous": 1,
    "stress": 1,
    "restless": 1,
    "uneasy": 1,
    "unsure": 1,
    "confuse": 1,
    "doubt": 1,
    "hesitate": 1,
    "stuck": 1,
    "fear": 1,
    "worried": 1,
    "miss": 1,
    "still": 1,
    "forget": 1,
    "thinking": 1,
    "checking": 1,
    "cling": 1,
    "scare": 1,
}


acceptance_words = {

    # HIGH
    "forgive": 3,
    "closure": 3,
    "rediscover": 3,
    "gratitude": 3,
    "grateful": 3,
    "unbothered": 3,
    "confident": 3,
    "proud": 3,
    "clarity": 3,

    # MEDIUM
    "accept": 2,
    "heal": 2,
    "peace": 2,
    "recover": 2,
    "independent": 2,
    "rebuild": 2,
    "forward": 2,
    "calm": 2,
    "free": 2,
    "growth": 2,
    "strong": 2,
    "release": 2,
    "relief": 2,
    "smile": 2,
    "happy": 2,
    "joy": 2,
    "comfortable": 2,
    "indifferent": 2,

    # LOW
    "move": 1,
    "okay": 1,
    "realize": 1,
    "learn": 1,
    "better": 1,
    "start": 1,
    "understand": 1,
    "grow": 1,
    "enough": 1,
    "change": 1,
    "finally": 1,
    "letting": 1,
    "finding": 1,
    "feeling": 1,
    "accepting": 1,
    "working": 1,
    "focusing": 1,
    "becoming": 1,
    "laugh": 1,
}


emotion_dict = {
    "anger": anger_words,
    "anxiety": anxiety_words,
    "acceptance": acceptance_words,
}


# BREAKUP CONTEXT KEYWORDS

breakup_anger_keywords = [
    "cheated",
    "cheating",
    "affair",
    "unfaithful",
    "lied to me",
    "betrayed",
    "betrayed my trust",
    "two timed",
    "manipulative",
    "gaslighting",
    "controlling",
    "toxic relationship",
    "emotionally abusive",
    "used me",
    "took advantage of me",
    "ghosted",
    "blocked me",
    "silent treatment",
    "red flag",
    "possessive",
    "ignored me",
    "argument",
    "argued",
    "fight",
    "fighting",
    "we fought",
    "constant fighting",
    "endless arguments"
]


breakup_anxiety_keywords = [
    "miss him",
    "miss her",
    "miss my ex",
    "still love",
    "still miss",
    "can not forget",
    "can not move on",
    "thinking about him",
    "thinking about her",
    "thinking about my ex",
    "i want him back",
    "i want her back",
    "i still care about him",
    "i still care about her",
    "overthinking him",
    "overthinking her",
    "relationship anxiety",
    "fear of losing",
    "afraid to lose him",
    "afraid to lose her",
    "worried he will leave",
    "worried she will leave",
    "attachment issues",
    "clingy",
    "insecure relationship",
    "heartbroken",
    "broken heart",
    "devastated",
    "shattered",
    "crushed",
    "lonely",
    "unloved",
    "unwanted",
    "lost him",
    "lost her",
    "crying over",
    "stalk my ex",
    "checking his profile",
    "checking her profile"
]


breakup_acceptance_keywords = [
    "healing",
    "recovering",
    "trying to move on",
    "self love",
    "letting go",
    "finding peace",
    "closure",
    "finally okay",
    "feeling better",
    "accepting the breakup",
    "learning to be alone",
    "working on myself",
    "focusing on myself",
    "becoming independent",
    "starting over",
    "fresh start",
    "new chapter",
    "new beginning",
    "getting over him",
    "getting over her",
    "slowly healing"
]

# TEXT CLEANING

def expand_contractions(text):

    def replace(match):
        token = match.group(0).lower()
        return CONTRACTIONS_DICT.get(token, token)

    return CONTRACTIONS_PATTERN.sub(replace, str(text))


def clean_text(text):

    text = str(text).lower()

    # remove URL
    text = re.sub(r"http\S+|www\S+", "", text)

    # expand contractions
    text = expand_contractions(text)

    # remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # remove numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# EMOTION PROCESSING

def preprocess_for_emotion(text):

    text = str(text).lower()

    text = re.sub(r"[^a-z\s]", " ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text.split()


def detect_structure_emotion(text):

    text = str(text).lower()

    scores = {
        "anger": 0,
        "anxiety": 0,
        "acceptance": 0
    }

    # anxiety
    if re.search(
        r"\b(why|what if|how could|where did|when will)\b",
        text
    ):
        scores["anxiety"] += 2

    # anger
    if re.search(
        r"\b(he lied|she lied|how dare|i hate|never again|so done)\b",
        text
    ):
        scores["anger"] += 2

    # acceptance
    if re.search(
        r"\b(i am okay|i am fine|i am better|i am moving|i am healing|i am done crying)\b",
        text
    ):
        scores["acceptance"] += 2

    # subject + negative action
    if re.search(
        r"\b(he|she)\b.{0,20}\b(left|lied|cheated|hurt|ignored|blocked|ghosted)\b",
        text
    ):
        scores["anger"] += 1

    # longing pattern
    if re.search(
        r"\bi\b.{0,20}\b(miss|wish|hope|want|need|think about)\b",
        text
    ):
        scores["anxiety"] += 1

    return scores


def calculate_emotion_probabilities(text):

    tokens = preprocess_for_emotion(text)

    token_counts = Counter(tokens)

    scores = {
        "anger": 0,
        "anxiety": 0,
        "acceptance": 0
    }

    # LAYER 1 — WEIGHTED LEXICON

    for emotion, vocab_dict in emotion_dict.items():

        for word, weight in vocab_dict.items():

            if word in token_counts:
                scores[emotion] += token_counts[word] * weight

    # LAYER 2 — BREAKUP CONTEXT

    text_lower = str(text).lower()

    for kw in breakup_anger_keywords:
        if kw in text_lower:
            scores["anger"] += 1

    for kw in breakup_anxiety_keywords:
        if kw in text_lower:
            scores["anxiety"] += 1

    for kw in breakup_acceptance_keywords:
        if kw in text_lower:
            scores["acceptance"] += 1

    # LAYER 3 — SENTENCE STRUCTURE

    structure_scores = detect_structure_emotion(text)

    for emotion in scores:
        scores[emotion] += structure_scores[emotion]

    # ACCEPTANCE PENALTY

    negative_strength = scores["anger"] + scores["anxiety"]

    if negative_strength > 0:
        scores["acceptance"] *= 0.35

    # SMOOTHING

    for emotion in scores:
        scores[emotion] += 0.01

    # SOFTMAX

    exp_scores = {
        e: np.exp(s)
        for e, s in scores.items()
    }

    total = sum(exp_scores.values())

    probs = {
        f"{e}_prob": exp_scores[e] / total
        for e in exp_scores
    }

    return pd.Series(probs)


# DATASET ASSESSMENT

def assess_data(df):

    print("\n" + "=" * 50)
    print("ASSESSING DATA")
    print("=" * 50)

    missing = df.isnull().sum()

    missing_df = pd.DataFrame({
        "jumlah_missing": missing,
        "persentase (%)": (missing / len(df) * 100).round(2)
    })

    print("\n[ Missing Value ]")
    print(missing_df)

    if "text" in df.columns:

        n_dup = df.duplicated(subset=["text"]).sum()

        print(f"\n[ Duplikat ]")
        print(f"Jumlah baris : {n_dup:,}")
        print(f"Persentase   : {n_dup / len(df) * 100:.2f}%")


# MAIN CLEANING PIPELINE

def clean_data(df):

    # remove missing
    df_clean = df.dropna(subset=["text"]).copy()

    # remove duplicates
    df_clean = (
        df_clean
        .drop_duplicates(subset=["text"])
        .reset_index(drop=True)
    )

    # clean text
    df_clean["text_clean"] = (
        df_clean["text"]
        .apply(clean_text)
    )

    # calculate emotion probabilities
    print("\n[i] Calculating emotion probabilities...")

    emotion_probs = (
        df_clean["text_clean"]
        .apply(calculate_emotion_probabilities)
    )

    # merge dataframe
    df_clean = pd.concat(
        [df_clean, emotion_probs],
        axis=1
    )

    return df_clean


# EXECUTABLE SCRIPT

if __name__ == "__main__":

    input_file = "nama_dataset_mentah_kamu.csv"

    try:

        print(f"Membaca data dari '{input_file}'...")

        df_raw = pd.read_csv(input_file)

        assess_data(df_raw)

        df_clean = clean_data(df_raw)

        output_file = "dataset_preprocessed.csv"

        df_clean.to_csv(output_file, index=False)

        print("\nSelesai!")
        print(f"Data disimpan di '{output_file}'")
        print(f"Jumlah data akhir: {len(df_clean):,}")

    except FileNotFoundError:

        print(f"\n[ERROR] File '{input_file}' tidak ditemukan.")
