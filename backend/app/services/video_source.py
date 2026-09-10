from __future__ import annotations

from urllib.parse import urlparse


VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".m4v",
    ".mpeg",
    ".mpg",
}


def detect_video_source(
    url: str,
) -> str:

    if not url:
        return "unknown"

    parsed = urlparse(url.strip())

    hostname = (
        parsed.hostname or ""
    ).lower()

    path = (
        parsed.path or ""
    ).lower()

    if (
        hostname == "youtube.com"
        or hostname.endswith(".youtube.com")
        or hostname == "youtu.be"
    ):
        return "youtube"

    if (
        hostname == "vimeo.com"
        or hostname.endswith(".vimeo.com")
    ):
        return "vimeo"

    extension = ""

    if "." in path:
        extension = "." + path.rsplit(".", 1)[-1]

    if extension in VIDEO_EXTENSIONS:
        return "direct"

    return "supported_url"