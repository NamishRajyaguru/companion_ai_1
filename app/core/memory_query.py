from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)

MEMORY_QUERY_PROMPT = """
You are a memory router.

Given a user message, return a JSON array of memory paths
needed to answer the question.

Memory structure hints:
- identity.name
- identity.birthday
- relationships.partner.name
- relationships.family
- context.life_phase
- context.current_focus
- critical
- identity.preferences.genres
- identity.preferences.music
- identity.preferences.movies
- identity.preferences.likes
- If the user asks about a friend, best friend, or mentions a known name, use context.important_people

Rules:
- Use dot notation
- If the user asks about boyfriend or partner, use relationships.partner.name
- If the user asks about mother or family, use relationships.family
- Return ONLY valid paths
- Return [] if no memory is needed
- Do NOT explain
"""

def get_required_memory_paths(user_text: str) -> list[str]:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": MEMORY_QUERY_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    import json

    try:
        parsed = json.loads(content)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []
