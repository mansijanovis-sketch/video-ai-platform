import re

from app.services.transcript_phrase_matcher import (
    find_phrase_across_segments,
)


def normalize_filename(text: str) -> str:
    text = text.strip().lower()

    # Normalize speech-to-text variants of ".js"
    text = re.sub(
        r"\b(j'?s|jas|j\s*/?\s*s)\b",
        ".js",
        text,
        flags=re.IGNORECASE,
    )

    # Remove punctuation except extension dot.
    text = re.sub(
        r"[^a-z0-9.\s_-]",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove existing .js extension.
    text = re.sub(
        r"\.js\b",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    words = re.findall(
        r"[a-z0-9]+",
        text,
        flags=re.IGNORECASE,
    )

    if not words:
        return ""

    filename = "".join(
        word.capitalize()
        for word in words
    )

    return f"{filename}.js"


def extract_created_file(
    text: str,
) -> str | None:

    patterns = [
        r"\bcreate\s+(?:a\s+)?new\s+file\s+called\s+(.+)",
        r"\bcreate\s+(?:a\s+)?new\s+file\s+named\s+(.+)",
        r"\bcreate\s+file\s+called\s+(.+)",
        r"\bcreate\s+file\s+named\s+(.+)",
        r"\bname\s+this\s+file\s+(.+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            filename_text = match.group(1)

            # Stop at common continuation words.
            filename_text = re.split(
                r"\b(?:and|then|here|with|for)\b",
                filename_text,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]

            filename = normalize_filename(
                filename_text
            )

            if filename:
                return filename

    return None


def extract_edited_file(
    text: str,
) -> str | None:

    patterns = [
        r"\b(?:replace|edit|update|open)\s+"
        r"([a-z0-9_-]+)"
        r"(?:\s+dot\s+|\s+)"
        r"(?:j'?s|jas|j\s*/?\s*s)\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return normalize_filename(
                match.group(1)
            )

    return None


def detect_edit_operation(
    text: str,
) -> str | None:

    text = text.lower()

    if re.search(
        r"\breplace\b",
        text,
    ):
        return "replace"

    if re.search(
        r"\b(edit|modify|change|update)\b",
        text,
    ):
        return "edit"

    if re.search(
        r"\bopen\b",
        text,
    ):
        return "open"

    return None


def build_context(
    ordered: list[dict],
    index: int,
    max_segments: int = 4,
) -> list[dict]:

    current = ordered[index]

    context_segments = [
        current
    ]

    for next_segment in ordered[
        index + 1:index + 1 + max_segments
    ]:

        gap = (
            float(next_segment["start_time"])
            - float(current["end_time"])
        )

        if gap > 5:
            break

        context_segments.append(
            next_segment
        )

    return context_segments


def extract_file_edit_actions(
    segments: list[dict],
) -> list[dict]:

    if not segments:
        return []

    ordered = sorted(
        segments,
        key=lambda item: item["start_time"],
    )

    actions = []
    processed = set()

    for index, segment in enumerate(ordered):

        context_segments = build_context(
            ordered,
            index,
        )

        context_text = " ".join(
            item.get("text", "").strip()
            for item in context_segments
            if item.get("text", "").strip()
        )

        if not context_text:
            continue

        # --------------------------------------------------
        # CREATE FILE
        # --------------------------------------------------

        created_file = extract_created_file(
            context_text
        )

        if created_file:

            key = (
                "create_file",
                created_file,
            )

            if key not in processed:

                processed.add(key)

                actions.append({
                    "action": "create_file",
                    "value": created_file,
                    "operation": "create",
                    "start_time": float(
                        context_segments[0]["start_time"]
                    ),
                    "end_time": float(
                        context_segments[-1]["end_time"]
                    ),
                    "evidence": context_text,
                    "confidence": 0.95,
                })

            continue

        # --------------------------------------------------
        # EDIT / REPLACE / OPEN FILE
        # --------------------------------------------------

        edited_file = extract_edited_file(
            context_text
        )

        if edited_file:

            operation = detect_edit_operation(
                context_text
            )

            if not operation:
                continue

            key = (
                "edit_file",
                edited_file,
                operation,
            )

            if key in processed:
                continue

            processed.add(key)

            actions.append({
                "action": "edit_file",
                "value": edited_file,
                "operation": operation,
                "start_time": float(
                    context_segments[0]["start_time"]
                ),
                "end_time": float(
                    context_segments[-1]["end_time"]
                ),
                "evidence": context_text,
                "confidence": 0.95,
            })

    actions.sort(
        key=lambda action: action["start_time"]
    )

    return actions