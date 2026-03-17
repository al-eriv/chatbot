import joblib
import re

CONFIDENCE_THRESHOLD = 0.55

model = joblib.load("models/intent_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")


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