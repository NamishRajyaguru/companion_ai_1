from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from app.core.memory_loader import load_memory
from app.core.summarizer import build_memory_summary
from app.core.memory_writer import write_memory
from app.utils.extractors import extract_reminder
from app.core.memory_query import get_required_memory_paths
from app.core.memory_loader import get_memory_by_path
from datetime import datetime
from app.services.reminders import (
    wants_to_save_reminder,
    asks_for_reminders,
    asks_to_clear_reminders,
    add_reminder_from_text,
    list_reminders,
    clear_all_reminders,
    prune_expired_reminders,
)
from app.services.chat_engine import generate_reply, bootstrap_messages


# ---------- CLIENT SETUP ----------
client = Groq(api_key=GROQ_API_KEY)

# ---------- LOAD MEMORY ----------
memory = load_memory()
memory_summary = build_memory_summary(memory)
pending_reminder = None
last_topic = None
memory.setdefault("critical", [])


# ---------- SYSTEM PROMPT ----------


# ---------- MESSAGE STATE ----------
messages = bootstrap_messages()
messages.append({
    "role": "assistant",
    "content": "Yeah, tell me. You okay?"
})



# ---------- HELPERS ----------

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
    return changed


def wants_to_save_memory(text: str) -> bool:
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

    return any(trigger in text for trigger in triggers)


def asks_for_reminders(text: str) -> bool:
    text = text.lower().strip()

    explicit_phrases = [
        "what are my reminders",
        "what are my reminder",
        "show reminders",
        "list reminders",
        "list my reminders",
        "tell me my reminders",
    ]

    return any(phrase == text or phrase in text for phrase in explicit_phrases)

def asks_to_clear_reminders(text: str) -> bool:
    text = text.lower().strip()
    phrases = [
        "clear reminders",
        "clear all reminders",
        "remove reminders",
        "delete reminders",
        "delete all reminders",
        "remove all reminders",
    ]
    return any(p in text for p in phrases)



# ---------- CHAT LOOP ----------
while True:
    user_input = input("You: ").strip()

    # ---- EXIT CLEANLY ----
    if user_input.lower() in ["exit", "quit"]:
        messages.append({
            "role": "user",
            "content": "I'm heading off now. Say bye naturally."
        })

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.9
        )

        reply = response.choices[0].message.content.strip()
        print("Companion:", reply)
        break

    # ---- EXPLICIT MEMORY SAVE (IDENTITY ONLY) ----
    if wants_to_save_reminder(user_input):
        if add_reminder_from_text(user_input):
            print("Companion: Got it. I’ll remember that. 👍")
        else:
            print("Companion: I think you want me to remember something, but I didn’t catch it clearly.")
        continue


    # ---- EXPLICIT FACT RETRIEVAL ----
    if asks_for_reminders(user_input):
        reminders = list_reminders()

        if not reminders:
            print("Companion: You don’t have any reminders saved.")
        else:
            print("Companion: Here’s what I’ve got:")
            for r in reminders:
                print(f"- {r}")
        continue


    # ---- MEMORY-AWARE RESPONSE ----
    paths = get_required_memory_paths(user_input)

    if paths:
        facts = {}

        for path in paths:
            value = get_memory_by_path(memory, path)
            if value is not None:
                facts[path] = value

        memory_context = "\n".join(
        f"- {path.replace('.', ' ')}: {value}"
        for path, value in facts.items()
        )

        messages.append({
        "role": "system",
        "content": f"Relevant known facts:\n{memory_context}"
        })



        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        print("Companion:", reply, "\n")
        messages.append({"role": "assistant", "content": reply})
        continue

    if asks_to_clear_reminders(user_input):
        clear_all_reminders()
        print("Companion: All reminders cleared. Clean slate 🤝")
        continue



    # ---- NORMAL CHAT ----
    reply = generate_reply(user_input, messages)
    print("Companion:", reply)
