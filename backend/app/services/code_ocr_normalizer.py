from __future__ import annotations

import re


COMMON_REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u00a0": " ",
}


COMMON_OCR_REPLACEMENTS = {
    "Conjponent": "Component",
    "componentWiltmMount": "componentWillMount",
    "componentWiliMount": "componentWillMount",
    "respanse": "response",
}


def normalize_quotes(text: str) -> str:
    """
    Convert typographic quotes into normal programming quotes.
    """

    for source, target in COMMON_REPLACEMENTS.items():
        text = text.replace(
            source,
            target,
        )

    return text


def normalize_common_ocr_errors(
    text: str,
) -> str:
    """
    Apply only high-confidence OCR corrections.

    These corrections are based on known programming
    identifiers rather than general spelling correction.
    """

    for source, target in COMMON_OCR_REPLACEMENTS.items():
        text = text.replace(
            source,
            target,
        )

    return text


def normalize_brackets_and_quotes(
    text: str,
) -> str:
    """
    Repair a small set of high-confidence OCR
    punctuation mistakes.

    We deliberately avoid aggressive punctuation
    modification because source code is punctuation-sensitive.
    """

    lines = []

    for line in text.splitlines():

        # OCR sometimes produces:
        #
        # constructor(props)'{
        #
        # where the quote is clearly an accidental
        # character before the opening brace.
        line = re.sub(
            r"(\))\s*'\s*\{",
            r"\1 {",
            line,
        )

        # Same issue with a double quote.
        line = re.sub(
            r'(\))\s*"\s*\{',
            r"\1 {",
            line,
        )

        # Normalize spaces immediately before opening braces.
        line = re.sub(
            r"\)\s*\{",
            ") {",
            line,
        )

        lines.append(line)

    return "\n".join(lines)


def normalize_whitespace(
    text: str,
) -> str:
    """
    Normalize excessive horizontal whitespace
    while preserving line structure.
    """

    lines = []

    for line in text.splitlines():

        line = line.rstrip()

        if not line.strip():
            lines.append("")
            continue

        line = re.sub(
            r"[ \t]+",
            " ",
            line,
        )

        lines.append(line)

    return "\n".join(lines)


def normalize_code_ocr(
    text: str,
) -> str:
    """
    Main OCR normalization pipeline.
    """

    if not text:
        return ""

    text = normalize_quotes(
        text
    )

    text = normalize_common_ocr_errors(
        text
    )

    text = normalize_brackets_and_quotes(
        text
    )

    text = normalize_whitespace(
        text
    )

    return text.strip()