from app.core.memory_query import get_required_memory_paths
from app.core.memory_loader import load_memory, get_memory_by_path


def get_memory_context(user_text: str) -> list[str]:
    """
    Determines which memory facts are required for a user query
    and returns them as formatted strings.

    Example return:
    [
        "identity name: Srishti",
        "identity boyfriend name: Namish"
    ]
    """

    memory = load_memory()
    paths = get_required_memory_paths(user_text)

    facts = []

    for path in paths:
        value = get_memory_by_path(memory, path)
        if value is not None:
            facts.append(f"{path.replace('.', ' ')}: {value}")

    return facts