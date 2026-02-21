from datetime import datetime
from app.utils.extractors import extract_reminder
from app.core.memory_writer import write_memory
from app.core.memory_loader import load_memory


# ---------- CLEANUP ----------

def prune_expired_reminders(memory: dict) -> bool:
    """Remove reminders whose date has passed. Returns True if changes were made."""
    today = datetime.now().date()
    reminders = memory.get("critical", [])

    kept = []
    changed = False

    for r in reminders:
        if r.get("date"):
            try:
                reminder_date = datetime.strptime(r["date"], "%Y-%m-%d").date()
                if reminder_date < today:
                    changed = True
                    continue
            except Exception:
                pass
        kept.append(r)

    if changed:
        memory["critical"] = kept
        write_memory(memory)

    return changed


# ---------- INTENT CHECKS ----------

def wants_to_save_reminder(text: str) -> bool:
    text = text.lower()

    if text.endswith("?"):
        return False

    triggers = [
        "remember",
        "don't forget",
        "do not forget",
        "save this",
        "note this",
        "keep this in mind",
        "remind me",
    ]

    return any(t in text for t in triggers)


def asks_for_reminders(text: str) -> bool:
    text = text.lower().strip()

    phrases = [
        "what are my reminders",
        "what are my reminder",
        "show reminders",
        "list reminders",
        "list my reminders",
        "tell me my reminders",
    ]

    return any(p in text for p in phrases)


def asks_to_clear_reminders(text: str) -> bool:
    text = text.lower()
    phrases = [
        "clear reminders",
        "clear all reminders",
        "remove reminders",
        "delete reminders",
        "delete all reminders",
        "remove all reminders",
    ]
    return any(p in text for p in phrases)


# ---------- ACTIONS ----------

def add_reminder_from_text(text: str) -> bool:
    """
    Tries to extract and save a reminder.
    Returns True if saved.
    """
    reminder = extract_reminder(text)
    if not reminder:
        return False

    memory = load_memory()
    memory.setdefault("critical", [])
    memory["critical"].append(reminder)
    write_memory(memory)
    return True


def list_reminders() -> list[str]:
    memory = load_memory()
    reminders = memory.get("critical", [])

    result = []
    for r in reminders:
        if r.get("raw_date"):
            result.append(f"{r['task']} on {r['raw_date']}")
        else:
            result.append(r["task"])

    return result


def clear_all_reminders():
    memory = load_memory()
    memory["critical"] = []
    write_memory(memory)