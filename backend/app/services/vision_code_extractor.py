from __future__ import annotations

import base64
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from backend/.env
load_dotenv()


DEFAULT_MODEL = os.getenv(
    "VISION_MODEL",
    "gpt-5.6-luna",
)


def encode_image(filepath: str) -> str:
    """
    Read an image file and convert it to base64.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"Image file does not exist: {filepath}"
        )

    if not path.is_file():
        raise ValueError(
            f"Image path is not a file: {filepath}"
        )

    with path.open("rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")


def extract_code_from_frame(
    filepath: str,
    timestamp: float | None = None,
    filename_hint: str | None = None,
) -> dict:
    """
    Analyze a single tutorial frame and extract visible code.

    The vision model is instructed to:
    - identify whether the frame contains code
    - identify the screen type
    - identify the filename
    - identify the programming language
    - transcribe only visible code
    - avoid inventing missing code
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not configured."
        )

    client = OpenAI(
        api_key=api_key
    )

    image_base64 = encode_image(filepath)

    prompt = """
You are analyzing a single frame from a programming tutorial video.

Your job is to extract ONLY information that is actually visible
in the frame.

The main goal is accurate extraction of source code from a code editor.

IMPORTANT RULES:

1. Do NOT invent code.
2. Do NOT complete missing code from your own knowledge.
3. Do NOT guess code that is outside the visible area.
4. Preserve the visible code as accurately as possible.
5. Preserve indentation when it is reasonably visible.
6. Preserve punctuation such as:
   - braces
   - parentheses
   - brackets
   - semicolons
   - quotes
   - commas
   - dots
   - operators
7. Ignore browser tabs and browser controls.
8. Ignore editor menus and toolbar buttons.
9. Ignore file explorer/sidebar content unless it helps identify
   the currently edited filename.
10. Ignore unrelated text outside the code editor.
11. If code is partially visible, return only the visible portion.
12. If text is uncertain, do not invent a replacement.
13. Identify the filename only when it is visible or strongly
    indicated by the editor UI.
14. Identify the programming language only when reasonably clear.
15. Return valid JSON only.
16. Do not wrap the JSON in markdown code fences.

Return exactly this JSON structure:

{
  "is_code_screen": true,
  "screen_type": "editor",
  "filename": "App.js",
  "language": "javascript",
  "code": "visible code here",
  "confidence": 0.0,
  "notes": "short explanation"
}

Allowed screen_type values:

- editor
- terminal
- browser
- mixed
- unknown

Rules for is_code_screen:

true:
- code editor is visible
- terminal containing commands/code is visible
- programming code is clearly visible

false:
- only browser/video content is visible
- no meaningful programming content is visible

Rules for code:

Return the actual visible source code.

Do not add:
- explanations
- comments that are not visible
- missing imports
- missing closing braces
- inferred code
- corrected code

If no meaningful code is visible:

{
  "is_code_screen": false,
  "screen_type": "unknown",
  "filename": null,
  "language": null,
  "code": "",
  "confidence": 0.0,
  "notes": "No meaningful code is visible."
}

Confidence:

0.90 - 1.00:
Very clear and readable.

0.70 - 0.89:
Mostly readable with some uncertainty.

0.50 - 0.69:
Partially readable.

Below 0.50:
Poor visibility or significant uncertainty.
"""

    if filename_hint:
        prompt += (
            "\n\nAdditional context:\n"
            f"The surrounding tutorial analysis suggests "
            f"the file may be '{filename_hint}'.\n"
            "Use this only as contextual evidence. "
            "Do not claim the filename is visible if it is not."
        )

    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                    {
                        "type": "input_image",
                        "image_url": (
                            "data:image/jpeg;base64,"
                            f"{image_base64}"
                        ),
                    },
                ],
            }
        ],
    )

    raw_text = response.output_text.strip()

    if not raw_text:
        raise ValueError(
            "Vision model returned an empty response."
        )

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Vision model returned invalid JSON:\n"
            f"{raw_text}"
        ) from exc

    # Validate the expected response structure.
    required_fields = [
        "is_code_screen",
        "screen_type",
        "filename",
        "language",
        "code",
        "confidence",
        "notes",
    ]

    missing_fields = [
        field
        for field in required_fields
        if field not in result
    ]

    if missing_fields:
        raise ValueError(
            "Vision model response is missing fields: "
            + ", ".join(missing_fields)
        )

    # Normalize a few fields so downstream code has
    # predictable data types.
    result["is_code_screen"] = bool(
        result["is_code_screen"]
    )

    result["code"] = (
        result["code"]
        if isinstance(result["code"], str)
        else str(result["code"] or "")
    )

    try:
        result["confidence"] = float(
            result["confidence"]
        )
    except (TypeError, ValueError):
        result["confidence"] = 0.0

    # Keep confidence inside the expected range.
    result["confidence"] = max(
        0.0,
        min(1.0, result["confidence"]),
    )

    result["filepath"] = filepath

    if timestamp is not None:
        result["timestamp"] = float(timestamp)

    return result