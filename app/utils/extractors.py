import re
from datetime import datetime, timedelta

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

def extract_birthday(text: str):
    """
    Extracts a birthday from text like:
    'my birthday is June 18'
    Returns dict or None
    """
    text = text.lower()

    for month, month_num in MONTHS.items():
        if month in text:
            match = re.search(rf"{month}\s+(\d{{1,2}})", text)
            if match:
                day = int(match.group(1))
                return {
                    "month": month_num,
                    "day": day,
                    "raw": f"{month.capitalize()} {day}"
                }

    return None

def extract_reminder(text: str):
    text_lower = text.lower()

    if (
        "remember" not in text_lower
        and "remind me" not in text_lower
        and "don't forget" not in text_lower
    ):
        return None

    date_match = re.search(
        r"(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})",
        text_lower
    )

    date = None
    raw_date = None

    if date_match:
        month_str, day = date_match.groups()
        month = MONTHS[month_str]
        year = datetime.now().year
        date = f"{year}-{month:02d}-{int(day):02d}"
        raw_date = f"{month_str.capitalize()} {day}"

    task = text_lower
    task = re.sub(r"(remind me|don't forget|remember to|remember i have|remember i|note this)", "", task)
    task = re.sub(
        r"(on|at)\s+(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}",
        "",
        task,
    )
    task = re.sub(r"(that|this|please|ayy)", "", task)
    task = task.strip(" ,.")
    task = re.sub(r"\s+", " ", task)

    if not task or len(task) < 3:
        return None

    return {
        "task": task,
        "date": date,
        "raw_date": raw_date,
        "created_at": datetime.utcnow().isoformat()
    }
