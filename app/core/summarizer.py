def build_memory_summary(memory: dict) -> str:
    """
    Builds a minimal, stable identity summary for the system prompt.
    This is NOT conversational memory.
    This is grounding only.
    """

    lines = []

    identity = memory.get("identity", {})
    preferences = identity.get("preferences", {})
    emotional = memory.get("emotional", {})
    relationships = memory.get("relationships", {})

    # --- Core identity ---
    name = identity.get("name")
    if name:
        lines.append(f"Her name is {name}.")

    # --- Communication style ---
    tone = preferences.get("tone")
    humour = preferences.get("humour")

    style_parts = []
    if tone:
        style_parts.append(tone)
    if humour:
        style_parts.append(humour)

    if style_parts:
        lines.append(f"She prefers a {', '.join(style_parts)} communication style.")

    # --- Emotional baseline (high level only) ---
    baseline = emotional.get("baseline")
    if baseline:
        lines.append("She is emotionally expressive and values conversation.")

    # --- Relationship status (NO names) ---
    partner = relationships.get("partner", {})
    if partner.get("status"):
        lines.append("She is in a relationship.")

    if not lines:
        return ""

    return "Known context:\n" + "\n".join(f"- {line}" for line in lines)