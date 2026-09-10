import re


CODE_PATTERNS = [
    r"\bimport\s+",
    r"\bfrom\s+['\"]",
    r"\bconst\s+\w+",
    r"\blet\s+\w+",
    r"\bvar\s+\w+",
    r"\bfunction\s+\w+",
    r"=>",
    r"\breturn\s*\(",
    r"\buseState\b",
    r"\buseEffect\b",
    r"\bReact\b",
    r"\bexport\s+default\b",
    r"\bclassName\s*=",
    r"</[A-Za-z]+>",
    r"\bpackage\.json\b",
    r"\.jsx\b",
    r"\.tsx\b",
    r"\.js\b",
    r"\.ts\b",
]


TERMINAL_PATTERNS = [
    r"\bnpm\s+(install|run|start|create)\b",
    r"\byarn\s+",
    r"\bpnpm\s+",
    r"\bgit\s+(clone|checkout|pull|push|add|commit)\b",
    r"\bpip\s+install\b",
    r"\bpython\s+",
    r"\bPS\s+[A-Z]:\\",
    r"[A-Z]:\\Users\\",
]


BROWSER_PATTERNS = [
    r"\bgoogle\.com\b",
    r"\byoutube\.com\b",
    r"\bchrome\b",
    r"\bSearch\b",
    r"\bVideos\b",
    r"\bImages\b",
    r"\bShopping\b",
    r"\bNews\b",
]


def matches_any(
    text: str,
    patterns: list[str],
) -> bool:

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE,
        ):
            return True

    return False


def classify_evidence(
    text: str,
) -> str:

    if not text:
        return "unknown"

    if matches_any(
        text,
        TERMINAL_PATTERNS,
    ):
        return "terminal"

    if matches_any(
        text,
        CODE_PATTERNS,
    ):
        return "code"

    if matches_any(
        text,
        BROWSER_PATTERNS,
    ):
        return "browser"

    return "ocr"


def get_evidence_confidence(
    evidence_type: str,
) -> float:

    confidence_map = {
        "code": 0.85,
        "terminal": 0.85,
        "browser": 0.90,
        "ocr": 0.50,
        "unknown": 0.20,
    }

    return confidence_map.get(
        evidence_type,
        0.20,
    )