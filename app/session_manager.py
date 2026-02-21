import json
from pathlib import Path

SESSION_FILE = Path(__file__).resolve().parent / "sessions" / "sessions.json"

def load_session():
    if not SESSION_FILE.exists():
        return []

    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data.get("default_user", {}).get("messages", [])

def save_session(messages):
    data = {
        "default_user": {
            "messages": messages
        }
    }

    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)