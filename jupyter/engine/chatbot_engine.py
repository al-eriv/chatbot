import joblib
import re
from pathlib import Path

CONFIDENCE_THRESHOLD = 0.55

# ruta base del archivo actual
BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR.parent / "models" / "intent_model.pkl"
VECTORIZER_PATH = BASE_DIR.parent / "models" / "vectorizer.pkl"

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def clean_text(text):

    text = text.lower()
    text = re.sub(r"[^a-záéíóúñ0-9 ]", " ", text)
    return text.strip()


def detect_intent(text):

    text = clean_text(text)

    vec = vectorizer.transform([text])

    probs = model.predict_proba(vec)[0]

    idx = probs.argmax()

    intent = model.classes_[idx]
    confidence = probs[idx]

    if confidence < CONFIDENCE_THRESHOLD:
        intent = "info_general"

    return intent