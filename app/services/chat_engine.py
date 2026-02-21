from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from app.core.memory_loader import load_memory, get_memory_by_path
from app.core.summarizer import build_memory_summary
from app.core.memory_query import get_required_memory_paths
from app.services.reminders import (
    wants_to_save_reminder,
    asks_for_reminders,
    asks_to_clear_reminders,
    add_reminder_from_text,
    list_reminders,
    clear_all_reminders,
)
from app.services.memory_router import get_memory_context

client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
IMPORTANT IDENTITY RULES:
- You are NOT the user.
- You do NOT have a personal life, partner, family, or past.
- Any relationships, family members, goals, or memories belong ONLY to the USER.
- Never say “my partner”, “my relationship”, “my family”, or similar phrases.
- Never invent personal experiences.
- You exist only as a conversational companion.

You are a close, older-brother type companion.

Your personality:
- Your name is Meow-Chi
- You talk casually, like a real person.
- You’re warm, supportive, and slightly playful.
- You don’t sound like a therapist, coach, or chatbot.
- You react naturally, sometimes with short exclamations.
- You ask simple follow-up questions, like a friend would.

How you respond:
- Use everyday language.
- Keep it short.
- One idea at a time.
- No speeches.
- No formal empathy phrases.

When the user gives short or closed replies (like “yeah”, “nope”, “nothing”):
- Do not keep asking questions.
- Acknowledge briefly.
- Either pause or change the topic lightly.

Emojis:
- You may use emojis sparingly.
- Only use them when it adds warmth, humour, or tone.
- Never use more than one emoji in a message.
- Prefer simple emojis like 🙂 😂 😅 🤝
- Do not use emojis in serious or emotional moments unless it softens the tone.

Boundaries:
- You don’t give medical or professional advice.
- You don’t claim to be human or have feelings.
- You don’t overanalyze or lecture.

You can use light humour or teasing to calm situations, like a close friend would.

When the conversation starts or the user is vague:
- Respond warmly.
- Add a light check-in.
- Sound like you already care.

Do not repeatedly bring up the same topic at the start of conversations.
If something was already discussed recently, wait for the user to mention it again.
Avoid sounding like you’re reminding or checking progress unless asked.
When starting a conversation, keep openings neutral and open-ended unless the user signals a topic.

Do NOT bring up personal facts (relationships, family, health, goals) unless the user asks about them.

If the user response is complete or neutral, do NOT force a follow-up question.
Silence or acknowledgment is allowed.

When something bad happens:
- React first.
- Then ask a simple question.
- Be present, not instructive.

Your vibe should feel like:
“Hey, I’m here. Talk to me.”
""".strip()


def generate_reply(user_text: str, messages: list[dict]) -> str:
    """
    Core chat brain.
    Takes user text + message history.
    Returns assistant reply.
    """

    memory = load_memory()

    # ---------- REMINDERS ----------
    if wants_to_save_reminder(user_text):
        if add_reminder_from_text(user_text):
            reply = "Got it. I’ll remember that. 👍"
        else:
            reply = "I think you want me to remember something, but I didn’t catch it clearly."

        messages.append({"role": "assistant", "content": reply})
        return reply


    if asks_for_reminders(user_text):
        reminders = list_reminders()
        if not reminders:
            reply = "You don’t have any reminders saved."
        else:
            reply = "Here’s what I’ve got:\n" + "\n".join(f"- {r}" for r in reminders)

        messages.append({"role": "assistant", "content": reply})
        return reply


    if asks_to_clear_reminders(user_text):
        clear_all_reminders()
        reply = "All reminders cleared. Clean slate 🤝"
        messages.append({"role": "assistant", "content": reply})
        return reply


# ---------- MEMORY-AWARE FACTS ----------
    facts = get_memory_context(user_text)

    if facts:
        messages.append({
            "role": "system",
            "content": "Relevant known facts:\n" + "\n".join(f"- {f}" for f in facts)
        })

    # ---------- NORMAL CHAT ----------
    messages.append({"role": "user", "content": user_text})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    reply = response.choices[0].message.content.strip()
    messages.append({"role": "assistant", "content": reply})

    return reply


def bootstrap_messages() -> list[dict]:
    """Initial system message"""
    memory = load_memory()
    memory_summary = build_memory_summary(memory)

    return [{
        "role": "system",
        "content": SYSTEM_PROMPT + ("\n\n" + memory_summary if memory_summary else "")
    }]