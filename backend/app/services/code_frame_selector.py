from __future__ import annotations

import os

import cv2


def validate_frame(
    frame: dict,
) -> dict:
    """
    Validate an extracted frame and collect basic metadata.
    """

    filepath = frame.get("filepath")

    if not filepath:
        return {
            **frame,
            "valid": False,
            "width": 0,
            "height": 0,
            "sharpness": 0.0,
        }

    if not os.path.exists(filepath):
        return {
            **frame,
            "valid": False,
            "width": 0,
            "height": 0,
            "sharpness": 0.0,
        }

    image = cv2.imread(filepath)

    if image is None:
        return {
            **frame,
            "valid": False,
            "width": 0,
            "height": 0,
            "sharpness": 0.0,
        }

    height, width = image.shape[:2]

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )

    sharpness = float(
        cv2.Laplacian(
            gray,
            cv2.CV_64F,
        ).var()
    )

    return {
        **frame,
        "valid": True,
        "width": width,
        "height": height,
        "sharpness": round(
            sharpness,
            2,
        ),
    }


def prepare_code_frames(
    frames: list[dict],
) -> list[dict]:
    """
    Validate all extracted frames and keep them in
    chronological order.

    We intentionally do not rank frames by visual
    heuristics here.

    The vision layer will determine which frames actually
    contain useful source code.
    """

    if not frames:
        return []

    validated = [
        validate_frame(frame)
        for frame in frames
    ]

    validated = [
        frame
        for frame in validated
        if frame["valid"]
    ]

    validated.sort(
        key=lambda frame: frame["timestamp"]
    )

    return validated


def select_chronological_frames(
    frames: list[dict],
    max_frames: int = 6,
) -> list[dict]:
    """
    Select evenly distributed frames across the coding
    interval.

    Chronological coverage is preferred because different
    frames may expose different portions of a source file.
    """

    prepared = prepare_code_frames(
        frames
    )

    if not prepared:
        return []

    if len(prepared) <= max_frames:
        return prepared

    total_frames = len(prepared)

    selected_indices = []

    for index in range(max_frames):

        position = round(
            index
            * (total_frames - 1)
            / (max_frames - 1)
        )

        selected_indices.append(
            int(position)
        )

    selected = [
        prepared[index]
        for index in selected_indices
    ]

    return selected