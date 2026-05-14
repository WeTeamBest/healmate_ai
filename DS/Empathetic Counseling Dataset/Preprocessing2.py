import re
import unicodedata
import numpy as np
import pandas as pd
from collections import Counter

# Hapus Duplikat, Pertahankan yang Pertama
df = df_full.drop_duplicates(
    subset=["input", "label"],
    keep="first"
).reset_index(drop=True)

# Cleaning Text & Expand contractions
contractions_dict = {
    # I (dengan apostrof)
    "i'm"       : "i am",
    "i've"      : "i have",
    "i'll"      : "i will",
    "i'd"       : "i would",
    # I (tanpa apostrof — typo/informal)
    "im"        : "i am",
    "ive"       : "i have",
    #"ill"       : "i will",   # hati-hati: "ill" juga berarti sakit
    #"id"        : "i would",  # hati-hati: "id" juga bisa noun
    # you
    "you're"    : "you are",
    "you've"    : "you have",
    "you'll"    : "you will",
    "you'd"     : "you would",
    "youre"     : "you are",
    "youve"     : "you have",
    "youll"     : "you will",
    "youd"      : "you would",
    # he
    "he's"      : "he is",
    "he'll"     : "he will",
    "he'd"      : "he would",
    "hes"       : "he is",
    "hed"       : "he would",
    # she
    "she's"     : "she is",
    "she'll"    : "she will",
    "she'd"     : "she would",
    "shes"      : "she is",
    "shed"      : "she would",
    # it
    "it's"      : "it is",
    "it'll"     : "it will",
    "it'd"      : "it would",
    #"its"       : "it is",    # hati-hati: "its" juga bisa possessive
    # we
    "we're"     : "we are",
    "we've"     : "we have",
    "we'll"     : "we will",
    "we'd"      : "we would",
    #"were"      : "we are",   # hati-hati: "were" juga past tense "be"
    "weve"      : "we have",
    "wed"       : "we would",
    # they
    "they're"   : "they are",
    "they've"   : "they have",
    "they'll"   : "they will",
    "they'd"    : "they would",
    "theyre"    : "they are",
    "theyve"    : "they have",
    "theyll"    : "they will",
    "theyd"     : "they would",
    # negations (dengan apostrof)
    "aren't"    : "are not",
    "isn't"     : "is not",
    "wasn't"    : "was not",
    "weren't"   : "were not",
    "don't"     : "do not",
    "doesn't"   : "does not",
    "didn't"    : "did not",
    "won't"     : "will not",
    "wouldn't"  : "would not",
    "can't"     : "can not",
    "cannot"    : "can not",
    "couldn't"  : "could not",
    "shouldn't" : "should not",
    "hadn't"    : "had not",
    "hasn't"    : "has not",
    "haven't"   : "have not",
    "mustn't"   : "must not",
    "needn't"   : "need not",
    "daren't"   : "dare not",
    "shan't"    : "shall not",
    # negations (tanpa apostrof — typo/informal)
    "arent"     : "are not",
    "isnt"      : "is not",
    "wasnt"     : "was not",
    "werent"    : "were not",
    "dont"      : "do not",
    "doesnt"    : "does not",
    "didnt"     : "did not",
    "wont"      : "will not",
    "wouldnt"   : "would not",
    "cant"      : "can not",
    "couldnt"   : "could not",
    "shouldnt"  : "should not",
    "hadnt"     : "had not",
    "hasnt"     : "has not",
    "havent"    : "have not",
    "mustnt"    : "must not",
    # have/would combinations (dengan apostrof)
    "that've"   : "that have",
    "who've"    : "who have",
    "would've"  : "would have",
    "could've"  : "could have",
    "should've" : "should have",
    "might've"  : "might have",
    "must've"   : "must have",
    # have/would combinations (tanpa apostrof)
    "wouldve"   : "would have",
    "couldve"   : "could have",
    "shouldve"  : "should have",
    "mightve"   : "might have",
    "mustve"    : "must have",
    # misc (dengan apostrof)
    "that's"    : "that is",
    "that'd"    : "that would",
    "there's"   : "there is",
    "there're"  : "there are",
    "there'll"  : "there will",
    "who's"     : "who is",
    "who'd"     : "who would",
    "who'll"    : "who will",
    "what's"    : "what is",
    "what're"   : "what are",
    "what'll"   : "what will",
    "what'd"    : "what did",
    "where's"   : "where is",
    "where'd"   : "where did",
    "when's"    : "when is",
    "why's"     : "why is",
    "how's"     : "how is",
    "how'd"     : "how did",
    "how'll"    : "how will",
    "let's"     : "let us",
    "y'all"     : "you all",
    # misc (tanpa apostrof)
    "thats"     : "that is",
    "theres"    : "there is",
    "whos"      : "who is",
    "whats"     : "what is",
    "wheres"    : "where is",
    "whens"     : "when is",
    "whys"      : "why is",
    "hows"      : "how is",
    "lets"      : "let us",
    "yall"      : "you all",
    # informal/slang
    "gonna"     : "going to",
    "wanna"     : "want to",
    "gotta"     : "got to",
    "kinda"     : "kind of",
    "sorta"     : "sort of",
    "dunno"     : "do not know",
    "ain't"     : "is not",
    "aint"      : "is not",
    "tryna"     : "trying to",
    "hafta"     : "have to",
    "oughta"    : "ought to",
    "supposta"  : "supposed to",
    "useta"     : "used to",
}

contractions_pattern = re.compile(
    r'\b(' + '|'.join(re.escape(k) for k in contractions_dict.keys()) + r')\b',
    re.IGNORdfASE
)

def expand_contractions(text):
    def replace(match):
        token = match.group(0).lower()
        return contractions_dict.get(token, token)
    return contractions_pattern.sub(replace, text)

# CLEANING FUNCTION V1
# mempertahankan punctuation

def clean_text_v1(text):

    # basic
    text = str(text).lower().strip()

    # normalize unicode
    text = unicodedata.normalize(
        "NFKD",
        text
    ).encode(
        "ascii",
        "ignore"
    ).ddfode(
        "utf-8",
        "ignore"
    )

    # hapus URL
    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    # ubah underscore jadi spasi
    text = re.sub(
        r"_+",
        " ",
        text
    )

    # expand contractions
    text = expand_contractions(text)

    # comma -> ,
    text = re.sub(
        r"\bcomma\b",
        ",",
        text
    )

    # tambah spasi setelah punctuation
    text = re.sub(
        r"([.,!?])([a-z0-9])",
        r"\1 \2",
        text
    )

    # hapus spasi sebelum punctuation
    text = re.sub(
        r"\s+([.,!?])",
        r"\1",
        text
    )

    # hapus karakter aneh
    text = re.sub(
        r"[^a-z0-9\s.,!?']",
        " ",
        text
    )

    # rapikan punctuation berulang
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)

    # rapikan titik/koma yang terpisah
    text = re.sub(
        r"\s+,",
        ",",
        text
    )

    # rapikan multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text

# CLEANING FUNCTION V2

def clean_text_v2(text):

    # gunakan hasil cleaning v1 dulu
    text = clean_text_v1(text)

    # hapus punctuation
    text = re.sub(
        r"[^\w\s]",
        " ",
        text
    )

    # hapus apostrophe tersisa
    text = re.sub(
        r"'",
        "",
        text
    )

    # rapikan multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text

# APPLY CLEANING

# input
df["input_clean"] = df["input"].apply(
    clean_text_v1
)

df["input_no_punct"] = df["input"].apply(
    clean_text_v2
)

# label
df["label_clean"] = df["label"].apply(
    clean_text_v1
)

df["label_no_punct"] = df["label"].apply(
    clean_text_v2
)

# PREVIEW
print(
    df[
        [
            "input_clean",
            "input_no_punct",
            "label_clean",
            "label_no_punct"
        ]
    ].head()
)

# Filter breakup score
breakup_keywords = [
    # RELATIONSHIP TERMS
    "boyfriend", "girlfriend", "bf", "gf", "partner",
    "husband", "wife", "fiance", "fiancee",
    "lover", "significant other", "spouse",
    "crush", "dating", "relationship",
    "romantic relationship", "long distance relationship",
    "ldr", "situationship",
    # BREAKUP TERMS
    "breakup", "break up", "broke up", "broken up",
    "split up", "ended things", "ended our relationship",
    "ended our friendship", "called it quits",
    "dumped", "got dumped", "left me", "left him",
    "left her", "walked away", "abandoned me",
    "moved on", "moving on", "separated",
    "divorce", "divorced", "separation",
    # EX / PAST RELATIONSHIP
    "my ex", "ex boyfriend", "ex girlfriend",
    "former boyfriend", "former girlfriend",
    "past relationship", "past lover",
    "previous relationship",
    # HEARTBREAK / LOSS
    "heartbroken", "broken heart", "hurt",
    "hurt me", "emotionally hurt",
    "devastated", "shattered", "crushed",
    "betrayed", "abandoned", "rejdfted",
    "unloved", "unwanted", "lonely",
    "miss him", "miss her", "miss my ex",
    "can not forget", "still love", "still miss",
    "lost him", "lost her", "can not move on",
    "crying over", "thinking about my ex",
    "thinking about him", "thinking about her",
    # CHEATING / BETRAYAL
    "cheated", "cheating", "affair",
    "unfaithful", "lied to me",
    "betrayed my trust", "two timed",
    "seeing someone else",
    "talking to another girl",
    "talking to another guy",
    # TOXIC RELATIONSHIP
    "toxic relationship", "manipulative",
    "emotionally abusive", "gaslight",
    "gaslighting", "controlling",
    "possessive", "ignored me",
    "ghosted", "blocked me",
    "silent treatment", "red flag",
    "used me", "took advantage of me",
    # ARGUMENT / CONFLICT
    "argument", "argued", "fight",
    "fighting", "fight with my boyfriend",
    "fight with my girlfriend",
    "constant fighting", "we fought",
    "we keep arguing", "misunderstanding",
    "conflict in relationship",
    # ANXIETY AFTER BREAKUP
    "overthinking him", "overthinking her",
    "anxious about relationship",
    "relationship anxiety", "fear of losing",
    "afraid to lose him", "afraid to lose her",
    "worried he will leave", "worried she will leave",
    "attachment issues", "clingy", "insdfure relationship",
    # ACCEPTANCE / HEALING
    "healing", "rdfovering", "trying to move on",
    "self love", "letting go", "finding peace", "closure",
    "finally okay", "feeling better", "accepting the breakup",
    "learning to be alone", "working on myself",
    "focusing on myself", "bdfoming independent",
    # SOCIAL MEDIA / MODERN TERMS
    "seen zoned", "friend zoned", "unfollowed me",
    "blocked me", "removed me", "texted my ex",
    "stalk my ex", "chdfking his profile", "chdfking her profile",
    # COMMON EXPRESSIONS
    "he does not love me", "she does not love me",
    "he stopped talking to me", "she stopped talking to me",
    "he lost feelings", "she lost feelings",
    "i miss my relationship", "i feel alone after breakup",
    "i can not stop thinking about him",
    "i can not stop thinking about her",
    "i want him back", "i want her back",
    "i still care about him", "i still care about her"
]

breakup_anger_keywords = [
    "cheated", "cheating", "affair", "unfaithful", "lied to me",
    "betrayed", "betrayed my trust", "two timed", "manipulative",
    "gaslighting", "controlling", "toxic relationship", "emotionally abusive",
    "used me", "took advantage of me", "ghosted", "blocked me",
    "silent treatment", "red flag", "possessive", "ignored me",
    "argument", "argued", "fight", "fighting", "we fought",
    "constant fighting", "endless arguments"
]

breakup_anxiety_keywords = [
    "miss him", "miss her", "miss my ex", "still love", "still miss",
    "can not forget", "can not move on", "thinking about him",
    "thinking about her", "thinking about my ex", "i want him back",
    "i want her back", "i still care about him", "i still care about her",
    "overthinking him", "overthinking her", "relationship anxiety",
    "fear of losing", "afraid to lose him", "afraid to lose her",
    "worried he will leave", "worried she will leave",
    "attachment issues", "clingy", "insdfure relationship",
    "heartbroken", "broken heart", "devastated", "shattered", "crushed",
    "lonely", "unloved", "unwanted", "lost him", "lost her",
    "crying over", "stalk my ex", "chdfking his profile", "chdfking her profile"
]

breakup_acceptance_keywords = [
    "healing", "rdfovering", "trying to move on", "self love",
    "letting go", "finding peace", "closure", "finally okay",
    "feeling better", "accepting the breakup", "learning to be alone",
    "working on myself", "focusing on myself", "bdfoming independent",
    "starting over", "fresh start", "new chapter", "new beginning",
    "getting over him", "getting over her", "slowly healing"
]

# BREAKUP SCORE FUNCTION
def get_breakup_score(text, keywords):

    text = str(text).lower()

    score = 0

    for keyword in keywords:

        pattern = (
            r"\b" +
            re.escape(keyword.lower()) +
            r"\b"
        )

        if re.search(pattern, text):

            score += 1

    return score


# HITUNG BREAKUP SCORE
# menggunakan kolom input_no_punct

df["breakup_score"] = df["input_no_punct"].apply(
    lambda x: get_breakup_score(
        x,
        breakup_keywords
    )
)

# FILTER DATA BREAKUP
# minimal mengandung 2 keyword breakup

df_breakup = df[
    df["breakup_score"] >= 2
].copy().reset_index(drop=True)


# INFORMASI FILTERING

print(f"Sebelum filter : {len(df):,} baris")

print(f"Sesudah filter : {len(df_breakup):,} baris")

print(
    f"Dihapus        : "
    f"{len(df) - len(df_breakup):,} baris"
)

# PREVIEW

print(
    df_breakup[
        [
            "input_clean",
            "breakup_score"
        ]
    ].head()
)

anger_words = [
    "mad",
    "pissed",
    "pissed off",
    "angry",
    "annoyed",
    "frustrated",
    "furious",
    "irritated",
    "bitter",
    "salty",
    "resentful",
    "hurt",
    "betrayed",
    "disappointed",
    "fed up",
    "done",
    "sick of it",
    "upset",
    "triggered",
    "grudge"
]

anxiety_words = [
    "anxious",
    "worried",
    "overthinking",
    "scared",
    "afraid",
    "nervous",
    "restless",
    "uneasy",
    "insdfure",
    "unsure",
    "confused",
    "paranoid",
    "stressed",
    "overwhelmed",
    "clingy",
    "doubtful",
    "hesitant",
    "obsessive",
    "stuck",
    "spiraling"
]

acceptance_words = [
    "move",
    "closure",
    "accept",
    "forgive",
    "heal",
    "let",
    "peace",
    "release",
    "okay",
    "realize",
    "learn",
    "better",
    "relief",
    "independent",
    "start",
    "strong",
    "understand",
    "grow",
    "enough",
    "change"
]

emotion_dict = {
    "anger": anger_words,
    "anxiety": anxiety_words,
    "acceptance": acceptance_words
}

# PREPROCESSING UNTUK EMOTION DETdfTION

def preprocess_for_emotion(text):

    text = str(text).lower()

    # hanya simpan huruf dan spasi
    text = re.sub(
        r"[^a-z\s]",
        " ",
        text
    )

    # rapikan spasi
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text.split()


# HEURISTIC BERDASARKAN STRUKTUR KALIMAT

def detdft_structure_emotion(text):

    text = str(text).lower()

    scores = {
        "anger": 0,
        "anxiety": 0,
        "acceptance": 0
    }

    # anxiety patterns

    if re.search(
        r"\b(why|what if|how could|where did|when will|should i|what do i do)\b",
        text
    ):
        scores["anxiety"] += 2

    # anger patterns

    if re.search(
        r"\b(he lied|she lied|how dare|i hate|never again|so done)\b",
        text
    ):
        scores["anger"] += 2

    # acceptance patterns

    if re.search(
        r"\b(i am okay|i am fine|i am better|i am moving on|i am healing|i am done crying)\b",
        text
    ):
        scores["acceptance"] += 2

    # he/she + negative action -> anger

    if re.search(
        r"\b(he|she)\b.{0,20}\b(left|lied|cheated|hurt|ignored|blocked|ghosted)\b",
        text
    ):
        scores["anger"] += 1

    # i + longing -> anxiety

    if re.search(
        r"\bi\b.{0,20}\b(miss|wish|hope|want|need|think about)\b",
        text
    ):
        scores["anxiety"] += 1

    return scores


# EMOTION PROBABILITY FUNCTION

def calculate_emotion_probabilities(text):

    tokens = preprocess_for_emotion(text)

    token_counts = Counter(tokens)

    scores = {
        "anger": 0,
        "anxiety": 0,
        "acceptance": 0
    }

    text_lower = str(text).lower()

    # LAYER 1
    
    for emotion, vocab_list in emotion_dict.items():

        for word in vocab_list:

            # multi-word keyword
            if " " in word:

                pattern = (
                    r"\b" +
                    re.escape(word.lower()) +
                    r"\b"
                )

                matches = re.findall(
                    pattern,
                    text_lower
                )

                scores[emotion] += len(matches)

            # single-word keyword
            else:

                if word in token_counts:

                    scores[emotion] += (
                        token_counts[word]
                    )

    # LAYER 2
    # breakup keyword context

    if all(score == 0 for score in scores.values()):

        for kw in breakup_anger_keywords:

            if re.search(
                r"\b" + re.escape(kw) + r"\b",
                text_lower
            ):
                scores["anger"] += 1

        for kw in breakup_anxiety_keywords:

            if re.search(
                r"\b" + re.escape(kw) + r"\b",
                text_lower
            ):
                scores["anxiety"] += 1

        for kw in breakup_acceptance_keywords:

            if re.search(
                r"\b" + re.escape(kw) + r"\b",
                text_lower
            ):
                scores["acceptance"] += 1

    # LAYER 3
    # sentence structure heuristic

    if all(score == 0 for score in scores.values()):

        structure_scores = detdft_structure_emotion(text)

        for emotion in scores:

            scores[emotion] += (
                structure_scores[emotion]
            )

    # BONUS / PENALTY

    # acceptance penalty
    negative_strength = (
        scores["anger"] +
        scores["anxiety"]
    )

    if negative_strength > 0:

        scores["acceptance"] *= 0.35

    # bonus anxiety jika banyak tanda tanya
    qmark_count = str(text).count("?")

    scores["anxiety"] += (
        qmark_count * 0.5
    )

    # bonus anger jika banyak tanda seru
    exclaim_count = str(text).count("!")

    scores["anger"] += (
        exclaim_count * 0.3
    )

    # TIE BREAKER

    # kalau semua skor 0
    if all(score == 0 for score in scores.values()):

        scores["anxiety"] += 0.05

    # SMOOTHING

    for emotion in scores:

        scores[emotion] += 0.01

    # SOFTMAX NORMALIZATION

    exp_scores = {
        emotion: np.exp(score)
        for emotion, score in scores.items()
    }

    total = sum(exp_scores.values())

    probs = {
        f"{emotion}_prob": (
            exp_scores[emotion] / total
        )
        for emotion in exp_scores
    }

    return pd.Series(probs)

# HITUNG PROBABILITAS EMOSI

print("\n[i] Menghitung probabilitas emosi...")

emotion_probs = df_breakup["input_clean"].apply(
    calculate_emotion_probabilities
)

emotion_cols = [
    "anger_prob",
    "anxiety_prob",
    "acceptance_prob"
]

# GABUNGKAN HASIL

df_eda = pd.concat(
    [
        df_breakup[
            [
                "input_clean",
                "label_clean",
                "input_no_punct",
                "label_no_punct",
                "breakup_score"
            ]
        ].reset_index(drop=True),

        emotion_probs.reset_index(drop=True)
    ],
    axis=1
)

# PREDICTED EMOTION

df_eda["predicted_emotion"] = (
    df_eda[emotion_cols]
    .idxmax(axis=1)
    .str.replace(
        "_prob",
        "",
        regex=False
    )
)

# EMOTION CONFIDENCE

df_eda["emotion_confidence"] = (
    df_eda[emotion_cols]
    .max(axis=1)
)

# FINAL DATASET

df_eda = df_eda[
    [
        "input_clean",
        "label_clean",
        "input_no_punct",
        "label_no_punct",
        "breakup_score",
        "anger_prob",
        "anxiety_prob",
        "acceptance_prob",
        "predicted_emotion",
        "emotion_confidence"
    ]
]

# PREVIEW

print(df_eda.head())

# Predicted emotion & confidence
CONFIDENCE_THRESHOLD = 0.34

def predict_emotion(row):
    probs = {
        "anger"      : row["anger_prob"],
        "anxiety"    : row["anxiety_prob"],
        "acceptance" : row["acceptance_prob"],
    }
    max_emotion = max(probs, key=probs.get)
    max_prob    = probs[max_emotion]

    if max_prob < CONFIDENCE_THRESHOLD:
        return "unclear"

    return max_emotion

df_eda["predicted_emotion"]  = df_eda.apply(predict_emotion, axis=1)
df_eda["emotion_confidence"] = df_eda[emotion_cols].max(axis=1)