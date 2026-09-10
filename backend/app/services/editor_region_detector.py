from __future__ import annotations

import os

import cv2


def detect_editor_region(
    filepath: str,
) -> dict:
    """
    Detect the likely source-code editor region
    in a programming tutorial frame.

    This is a deterministic first version.

    The goal is to remove:
    - browser content
    - application chrome
    - file explorer/sidebar

    and retain the main code editor.
    """

    if not filepath:
        raise ValueError(
            "Frame filepath is required."
        )

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Frame does not exist: {filepath}"
        )

    image = cv2.imread(filepath)

    if image is None:
        raise ValueError(
            f"Could not read frame: {filepath}"
        )

    height, width = image.shape[:2]

    # ---------------------------------------------------------
    # Coding tutorials commonly have:
    #
    #   browser / preview
    #   file explorer
    #   code editor
    #
    # For our current tutorial, the code editor occupies
    # approximately the right 60% of the frame.
    #
    # We intentionally remove the left-side UI because
    # OCR accuracy is more important than preserving the
    # file explorer.
    # ---------------------------------------------------------

    left = int(width * 0.50)
    right = int(width * 0.99)

    top = int(height * 0.02)
    bottom = int(height * 0.98)

    crop = image[
        top:bottom,
        left:right,
    ]

    crop_height, crop_width = crop.shape[:2]

    return {
        "filepath": filepath,
        "x": left,
        "y": top,
        "width": crop_width,
        "height": crop_height,
        "original_width": width,
        "original_height": height,
    }


def crop_editor_region(
    filepath: str,
    region: dict,
    output_filepath: str,
) -> str:
    """
    Crop and save the detected editor region.
    """

    image = cv2.imread(filepath)

    if image is None:
        raise ValueError(
            f"Could not read frame: {filepath}"
        )

    x = int(region["x"])
    y = int(region["y"])
    width = int(region["width"])
    height = int(region["height"])

    x2 = min(
        x + width,
        image.shape[1],
    )

    y2 = min(
        y + height,
        image.shape[0],
    )

    cropped = image[
        y:y2,
        x:x2,
    ]

    if cropped.size == 0:
        raise ValueError(
            "Editor crop produced an empty image."
        )

    output_dir = os.path.dirname(
        output_filepath
    )

    if output_dir:
        os.makedirs(
            output_dir,
            exist_ok=True,
        )

    success = cv2.imwrite(
        output_filepath,
        cropped,
    )

    if not success:
        raise ValueError(
            f"Could not save editor crop: "
            f"{output_filepath}"
        )

    return output_filepath