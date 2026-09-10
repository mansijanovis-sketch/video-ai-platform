from __future__ import annotations

import os
import uuid
from pathlib import Path
from urllib.parse import urlparse

import requests
import yt_dlp

from ..config import UPLOAD_DIR
from .video_source import detect_video_source


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


def _extension_from_url(
    url: str,
) -> str:

    path = urlparse(url).path.lower()

    extension = Path(path).suffix

    if extension in VIDEO_EXTENSIONS:
        return extension

    return ".mp4"


def _download_direct_video(
    url: str,
) -> dict:

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True,
    )

    extension = _extension_from_url(url)

    filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    filepath = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    response = requests.get(
        url,
        stream=True,
        timeout=60,
    )

    response.raise_for_status()

    content_type = (
        response.headers.get(
            "content-type",
            "",
        ).lower()
    )

    if (
        not content_type.startswith("video/")
        and extension not in VIDEO_EXTENSIONS
    ):
        raise ValueError(
            "The URL does not appear to point "
            "to a video file."
        )

    with open(
        filepath,
        "wb",
    ) as output:

        for chunk in response.iter_content(
            chunk_size=1024 * 1024,
        ):

            if chunk:
                output.write(chunk)

    return {
        "filepath": filepath,
        "title": Path(filepath).stem,
        "source_type": "direct",
    }


def _download_with_ytdlp(
    url: str,
) -> dict:

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True,
    )

    output_template = os.path.join(
        UPLOAD_DIR,
        "%(id)s.%(ext)s",
    )

    options = {
        "quiet": True,
        "noplaylist": True,
        "outtmpl": output_template,
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(options) as ydl:

        info = ydl.extract_info(
            url,
            download=True,
        )

    video_id = info.get("id")

    extension = info.get("ext") or "mp4"

    filepath = os.path.join(
        UPLOAD_DIR,
        f"{video_id}.{extension}",
    )

    if not os.path.exists(filepath):

        candidates = [
            os.path.join(
                UPLOAD_DIR,
                name,
            )
            for name in os.listdir(
                UPLOAD_DIR
            )
            if name.startswith(
                f"{video_id}."
            )
        ]

        if candidates:
            filepath = candidates[0]

    return {
        "filepath": filepath,
        "title": info.get("title"),
        "duration": info.get("duration"),
        "fps": info.get("fps"),
        "width": info.get("width"),
        "height": info.get("height"),
        "source_type": detect_video_source(url),
        "external_id": video_id,
    }


def acquire_video_from_url(
    url: str,
) -> dict:

    source_type = detect_video_source(
        url
    )

    if source_type == "direct":
        return _download_direct_video(url)

    return _download_with_ytdlp(url)