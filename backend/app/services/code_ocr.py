from __future__ import annotations

import os
from pathlib import Path

import cv2
import pytesseract

from app.config import TESSERACT_PATH


def preprocess_code_image(
    filepath: str,
    scale: float = 2.0,
) -> dict:
    """
    Prepare a code-editor crop for OCR.

    Returns multiple preprocessed versions so we can
    compare OCR quality instead of relying on one
    preprocessing strategy.
    """

    if not filepath:
        raise ValueError(
            "Image filepath is required."
        )

    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"Image does not exist: {filepath}"
        )

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(
            f"Could not read image: {filepath}"
        )

    height, width = image.shape[:2]

    new_width = int(width * scale)
    new_height = int(height * scale)

    enlarged = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_CUBIC,
    )

    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY,
    )

    # Mild contrast enhancement.
    contrast = cv2.equalizeHist(gray)

    # OTSU threshold.
    _, otsu = cv2.threshold(
        contrast,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    # Adaptive threshold.
    adaptive = cv2.adaptiveThreshold(
        contrast,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    # Sharpen the grayscale image.
    blurred = cv2.GaussianBlur(
        gray,
        (0, 0),
        3,
    )

    sharpened = cv2.addWeighted(
        gray,
        1.5,
        blurred,
        -0.5,
        0,
    )

    return {
        "original": enlarged,
        "grayscale": gray,
        "contrast": contrast,
        "otsu": otsu,
        "adaptive": adaptive,
        "sharpened": sharpened,
    }


def save_preprocessed_images(
    images: dict,
    output_dir: str,
    prefix: str = "code",
) -> dict:
    """
    Save all preprocessing variants for inspection.
    """

    os.makedirs(
        output_dir,
        exist_ok=True,
    )

    saved = {}

    for name, image in images.items():
        filepath = os.path.join(
            output_dir,
            f"{prefix}_{name}.png",
        )

        success = cv2.imwrite(
            filepath,
            image,
        )

        if not success:
            raise ValueError(
                f"Could not save image: {filepath}"
            )

        saved[name] = filepath

    return saved


def run_tesseract(
    image,
    psm: int = 6,
) -> str:
    """
    Run Tesseract against a preprocessed code image.
    """

    if image is None:
        return ""

    if TESSERACT_PATH:
        pytesseract.pytesseract.tesseract_cmd = (
            TESSERACT_PATH
        )

    config = f"--psm {psm}"

    text = pytesseract.image_to_string(
        image,
        config=config,
    )

    return text.strip()


def extract_code_ocr_candidates(
    filepath: str,
) -> dict:
    """
    Run OCR using multiple preprocessing strategies.

    This intentionally returns all candidates.
    We will build a code-aware selector later.
    """

    images = preprocess_code_image(
        filepath
    )

    results = {}

    for name, image in images.items():
        results[name] = {
            "psm_6": run_tesseract(
                image,
                psm=6,
            ),
            "psm_11": run_tesseract(
                image,
                psm=11,
            ),
        }

    return results