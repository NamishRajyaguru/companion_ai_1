import json 
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent.parent / "memory" / "memory.json"

def load_memory():
    """
    Loads the entire memory store from disk.
    Read-only. No mutation here.
    """
    if not MEMORY_FILE.exists():
        raise FileNotFoundError("memory.json not found")
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_memory_by_path(memory: dict, path: str):
    current = memory
    for key in path.split("."):
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current