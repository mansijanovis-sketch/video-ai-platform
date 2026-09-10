import re


NON_SPEECH_PATTERNS = [
    r"^\[music\]$",
    r"^\[applause\]$",
    r"^\[laughter\]$",
    r"^\[cheering\]$",
    r"^\[silence\]$",
]


def is_useful_transcript_text(
    text: str,
) -> bool:

    text = text.strip()

    if not text:
        return False

    normalized = text.lower()

    for pattern in NON_SPEECH_PATTERNS:
        if re.match(
            pattern,
            normalized,
        ):
            return False

    return True


def clean_youtube_segments(
    segments: list[dict],
) -> list[dict]:

    cleaned = []

    for segment in segments:

        text = segment.get(
            "text",
            "",
        ).strip()

        if not is_useful_transcript_text(
            text
        ):
            continue

        cleaned.append(
            {
                "start_time": float(
                    segment["start_time"]
                ),
                "end_time": float(
                    segment["end_time"]
                ),
                "text": text,
            }
        )

    return cleaned