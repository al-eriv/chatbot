import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_flows():
    with open(BASE_DIR / "flows.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_flows(flows):
    with open(BASE_DIR / "flows.json", "w", encoding="utf-8") as f:
        json.dump(flows, f, indent=2, ensure_ascii=False)