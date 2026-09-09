import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def is_reasonable_text(text: str) -> bool:
    text = text.strip()

    if not text:
        return False

    # Ignore extremely short fragments
    if len(text) < 4:
        return False

    # Number of alphabetic characters
    letters = sum(char.isalpha() for char in text)

    # Number of alphanumeric characters
    alphanumeric = sum(char.isalnum() for char in text)

    if letters < 2:
        return False

    if len(text) > 0:
        ratio = alphanumeric / len(text)

        # Mostly symbols = probably OCR noise
        if ratio < 0.50:
            return False

    # Reject obvious browser/UI garbage
    garbage_patterns = [
        r"^[<>@+\-_=~|]+$",
        r"^[A-Z]{1,3}$",
        r"^[a-z]{1,2}$",
    ]

    for pattern in garbage_patterns:
        if re.match(pattern, text):
            return False

    return True


def extract_text(image_path: str) -> str:
    image = cv2.imread(image_path)

    if image is None:
        return ""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(
        gray,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC,
    )

    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )[1]

    data = pytesseract.image_to_data(
        processed,
        lang="eng",
        config="--psm 11",
        output_type=pytesseract.Output.DICT,
    )

    lines = {}

    total = len(data["text"])

    for i in range(total):

        text = data["text"][i].strip()

        if not text:
            continue

        try:
            confidence = float(data["conf"][i])
        except (ValueError, TypeError):
            continue

        if confidence < 55:
            continue

        block_num = data["block_num"][i]
        par_num = data["par_num"][i]
        line_num = data["line_num"][i]

        key = (
            block_num,
            par_num,
            line_num,
        )

        if key not in lines:
            lines[key] = []

        lines[key].append({
            "text": text,
            "confidence": confidence,
            "left": data["left"][i],
        })

    valid_lines = []

    for words in lines.values():

        words.sort(
            key=lambda item: item["left"]
        )

        line_text = " ".join(
            item["text"]
            for item in words
        )

        average_confidence = (
            sum(
                item["confidence"]
                for item in words
            )
            / len(words)
        )

        if average_confidence < 55:
            continue

        if not is_reasonable_text(line_text):
            continue

        valid_lines.append(line_text)

    # Remove duplicates
    unique_lines = []
    seen = set()

    for line in valid_lines:

        normalized = re.sub(
            r"\s+",
            " ",
            line,
        ).strip()

        key = normalized.lower()

        if key in seen:
            continue

        seen.add(key)
        unique_lines.append(normalized)

    return "\n".join(unique_lines)