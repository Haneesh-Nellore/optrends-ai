# feedback_nlp_ai.py
# Phase 3: AI Sentiment + Keyphrases + Topic Clusters

import pandas as pd
from pathlib import Path

from transformers import pipeline
from keybert import KeyBERT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ---------- Paths ----------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CLEANED = BASE_DIR / "Clean_Datasets"

FEEDBACK_PATH = DATA_CLEANED / "Feedback_Cleaned.csv"
OUTPUT_PATH = DATA_CLEANED / "Feedback_AI_Final.csv"

print("Loading:", FEEDBACK_PATH)

# ---------- Load data ----------
df = pd.read_csv(FEEDBACK_PATH)
df = df.copy()
df["Free_Text"] = df["Free_Text"].fillna("")

# If you want to test fast, uncomment this line:
# df = df.head(300).copy()

print("Rows:", len(df))

# ---------- 1. Sentiment (HuggingFace) ----------
print("Loading sentiment model...")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_sentiment(text: str):
    # Return Neutral if empty text
    if not isinstance(text, str) or not text.strip():
        return pd.Series(["Neutral", 0.0])

    # Truncate very long text so model doesn't crash
    # {'label': 'POSITIVE', 'score': 0.98}
    result = sentiment_model(text[:512])[0]
    label = result["label"].capitalize()     # Positive / Negative
    score = float(result["score"])

    if label not in ["Positive", "Negative"]:
        label = "Neutral"

    return pd.Series([label, score])


print("Running sentiment...")
df[["Sentiment_Label", "Sentiment_Score"]
   ] = df["Free_Text"].apply(analyze_sentiment)

# ---------- 2. Key Phrases (KeyBERT) ----------
print("Loading KeyBERT model...")
kw_model = KeyBERT()


def extract_phrases(text: str, top_n: int = 3) -> str:
    if not isinstance(text, str) or not text.strip():
        return ""
    try:
        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),
            stop_words="english",
            top_n=top_n
        )
        phrases = [kw for kw, score in keywords]
        return ", ".join(phrases)
    except Exception:
        return ""


print("Extracting key phrases...")
df["Key_Phrases"] = df["Free_Text"].apply(
    lambda x: extract_phrases(x, top_n=3))

# ---------- 3. Topic Clusters (KMeans on key phrases) ----------
print("Clustering topics...")
texts_for_clustering = df["Key_Phrases"].fillna("")

vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(texts_for_clustering)

n_clusters = 5  # you can change to 4/6/etc

if X.shape[0] >= n_clusters:
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    df["Topic_Cluster"] = clusters
else:
    df["Topic_Cluster"] = 0  # fallback if very few rows

# ---------- Save result ----------
df.to_csv(OUTPUT_PATH, index=False)
print("✅ Saved AI-enriched feedback to:", OUTPUT_PATH)
