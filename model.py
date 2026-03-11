# model.py
# -------------------------------------------------------
# Trains a job-role classification model on dataset.csv
# and exposes a predict() function for inference.
#
# Pipeline:
#   Raw skills text
#       → TF-IDF Vectorizer
#       → Logistic Regression (primary) / Naive Bayes (fallback)
#       → Predicted job role + confidence scores
# -------------------------------------------------------

import os
import pickle
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# Paths
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATASET    = os.path.join(BASE_DIR, "dataset.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "job_classifier.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_model(save: bool = True) -> Pipeline:
    """
    Load dataset, train a TF-IDF + Logistic Regression pipeline,
    and optionally persist it to disk.

    Returns:
        Trained sklearn Pipeline.
    """
    print("[Model] Loading dataset …")
    df = pd.read_csv(DATASET)
    df.dropna(inplace=True)
    df.columns = df.columns.str.strip()

    X = df["skills"].astype(str)
    y = df["job_role"].astype(str)

    # Show class distribution
    print("[Model] Class distribution:")
    for role, count in y.value_counts().items():
        print(f"         {role}: {count}")

    # Build pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),   # unigrams + bigrams
            max_features=3000,
            sublinear_tf=True,    # apply log(TF) scaling
        )),
        ("clf", LogisticRegression(
            max_iter=1000,
            C=5.0,
            solver="lbfgs",
        )),
    ])

    # Cross-validation to check generalisation
    if len(X) >= 10:
        cv_scores = cross_val_score(pipeline, X, y, cv=min(5, len(X) // 3), scoring="accuracy")
        print(f"[Model] CV accuracy: {cv_scores.mean():.2%} ± {cv_scores.std():.2%}")

    # Final fit on all data
    pipeline.fit(X, y)

    if save:
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(pipeline, f)
        print(f"[Model] Saved to {MODEL_PATH}")

    return pipeline


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_model() -> Pipeline:
    """
    Load the trained model from disk, training it first if necessary.

    Returns:
        Trained sklearn Pipeline.
    """
    if not os.path.exists(MODEL_PATH):
        print("[Model] No saved model found — training now …")
        return train_model(save=True)

    with open(MODEL_PATH, "rb") as f:
        pipeline = pickle.load(f)
    print("[Model] Loaded existing model.")
    return pipeline


# ---------------------------------------------------------------------------
# Inference
# ---------------------------------------------------------------------------

def predict(skills: list, pipeline: Pipeline = None) -> dict:
    """
    Predict job role from a list of skills.

    Args:
        skills  : List of detected skill strings.
        pipeline: Pre-loaded pipeline (loaded on first call if None).

    Returns:
        Dict with keys:
            'job_role'      – top predicted role (str)
            'confidence'    – probability of top prediction (float 0-1)
            'all_scores'    – list of {role, score} for all classes
    """
    global _CACHED_MODEL
    if pipeline is None:
        if "_CACHED_MODEL" not in globals() or _CACHED_MODEL is None:
            _CACHED_MODEL = load_model()
        pipeline = _CACHED_MODEL

    # Join skills into a single string for vectorisation
    skills_text = " ".join(skills) if skills else "unknown"

    # Probabilities for all classes
    proba = pipeline.predict_proba([skills_text])[0]
    classes = pipeline.classes_

    # Sort by probability descending
    sorted_idx = np.argsort(proba)[::-1]
    all_scores = [
        {"role": classes[i], "score": round(float(proba[i]), 4)}
        for i in sorted_idx
    ]

    top_role  = classes[sorted_idx[0]]
    top_score = float(proba[sorted_idx[0]])

    return {
        "job_role":   top_role,
        "confidence": round(top_score, 4),
        "all_scores": all_scores,
    }


# Cache slot
_CACHED_MODEL = None


# ---------------------------------------------------------------------------
# CLI entry point — run `python model.py` to (re)train
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Training Job Role Classifier ===")
    pipe = train_model(save=True)

    # Quick smoke test
    test_cases = [
        (["Python", "Machine Learning", "TensorFlow", "Deep Learning"], "ML Engineer"),
        (["React", "JavaScript", "HTML", "CSS", "TypeScript"],          "Frontend Developer"),
        (["Java", "Spring Boot", "SQL", "REST API", "Docker"],          "Backend Developer"),
        (["AWS", "Docker", "Kubernetes", "CI/CD", "Terraform"],         "DevOps Engineer"),
    ]

    print("\n=== Smoke Tests ===")
    for skills, expected in test_cases:
        result = predict(skills, pipe)
        status = "✓" if result["job_role"] == expected else "✗"
        print(f" {status} [{expected}]  →  Predicted: {result['job_role']}  ({result['confidence']:.0%})")
