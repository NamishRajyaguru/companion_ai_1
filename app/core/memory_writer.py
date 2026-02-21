import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path(__file__).resolve().parent.parent / "memory" / "memory.json"


def write_memory(updated_memory: dict):
    """Overwrites memory.json safely."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(updated_memory, f, indent=2, ensure_ascii=False)


def update_memory_path(memory: dict, path: list[str], value):
    """
    Updates a nested path inside memory safely.
    Example path: ["relationships", "partner", "name"]
    """
    current = memory

    for key in path[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    current[path[-1]] = value
    memory["meta"]["last_memory_update"] = datetime.utcnow().isoformat()
    write_memory(memory)