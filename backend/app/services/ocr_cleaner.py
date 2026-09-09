import re


def clean_ocr_text(text: str) -> str:
    if not text:
        return ""

    cleaned, seen = [], set()
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip(" .|,;:-_")
        alphanumeric = sum(char.isalnum() for char in line)
        if len(line) < 4 or alphanumeric < 3 or alphanumeric / max(len(line), 1) < 0.55:
            continue
        key = re.sub(r"[^a-z0-9]+", "", line.lower())
        if key and key not in seen:
            seen.add(key)
            cleaned.append(line)
    return "\n".join(cleaned)
