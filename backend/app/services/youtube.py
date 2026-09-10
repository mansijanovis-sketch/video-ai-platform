import re


YOUTUBE_PATTERNS = [
    r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
    r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
    r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
]


def extract_youtube_video_id(
    url: str,
) -> str | None:

    if not url:
        return None

    url = url.strip()

    for pattern in YOUTUBE_PATTERNS:

        match = re.search(
            pattern,
            url,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

    return None


def is_valid_youtube_url(
    url: str,
) -> bool:

    return (
        extract_youtube_video_id(url)
        is not None
    )