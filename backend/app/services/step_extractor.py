import re


IGNORE_PATTERNS = [
    r"\bcredit operation\b",
    r"\bcrud operation\b",
    r"\bmost of the applications\b",
    r"\bwe use\b",
    r"\bget all\b",
    r"\bget by id\b",
    r"\bgo to visual studio code\b",
]


def is_relevant_text(text: str) -> bool:
    text_lower = text.lower()

    for pattern in IGNORE_PATTERNS:
        if re.search(pattern, text_lower):
            return False

    return True


def build_evidence(segment: dict) -> dict:
    return {
        "source": "transcript",
        "start_time": segment["start_time"],
        "end_time": segment["end_time"],
        "text": segment["text"],
    }


def extract_folder_name(text: str):
    match = re.search(
        r"(?:folder|directory).*?(?:name|called)\s+([A-Za-z0-9_-]+)",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_file_name(text: str):
    match = re.search(
        r"(?:file|name)\s+(?:and\s+give\s+it\s+a\s+name\s+)?([A-Za-z0-9_.-]+\.js)",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_array_name(text: str):
    match = re.search(
        r"(?:array|declare\s+(?:a|an)\s+array)\s+([A-Za-z_][A-Za-z0-9_]*)",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1)

    return None


def extract_steps(
    transcript_segments: list[dict],
) -> list[dict]:

    steps = []

    for segment in transcript_segments:

        text = segment.get(
            "text",
            "",
        ).strip()

        if not text:
            continue

        if not is_relevant_text(text):
            continue

        text_lower = text.lower()

        # -------------------------------------------------
        # CREATE FOLDER
        # -------------------------------------------------

        if (
            "create a new folder" in text_lower
            or "create new folder" in text_lower
        ):

            folder_name = extract_folder_name(
                text
            )

            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "create_folder",
                    "name": folder_name,
                    "path": (
                        f"src/{folder_name}"
                        if folder_name
                        else None
                    ),
                    "instruction": text,
                    "start_time": segment[
                        "start_time"
                    ],
                    "end_time": segment[
                        "end_time"
                    ],

                    "confidence": 0.65,
                    "verified": False,

                    "evidence": build_evidence(
                        segment
                    ),
                }
            )

            continue

        # -------------------------------------------------
        # CREATE FILE
        # -------------------------------------------------

        if (
            "create a new file" in text_lower
            or "create new file" in text_lower
        ):

            file_name = extract_file_name(
                text
            )

            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "create_file",
                    "name": file_name,
                    "path": (
                        f"src/components/{file_name}"
                        if file_name
                        else None
                    ),
                    "instruction": text,
                    "start_time": segment[
                        "start_time"
                    ],
                    "end_time": segment[
                        "end_time"
                    ],

                    "confidence": 0.65,
                    "verified": False,

                    "evidence": build_evidence(
                        segment
                    ),
                }
            )

            continue

        # -------------------------------------------------
        # DEFINE ARRAY
        # -------------------------------------------------

        if (
            "declare" in text_lower
            and "array" in text_lower
        ):

            array_name = extract_array_name(
                text
            )

            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "define_array",
                    "name": array_name,
                    "path": None,
                    "instruction": text,
                    "start_time": segment[
                        "start_time"
                    ],
                    "end_time": segment[
                        "end_time"
                    ],

                    "confidence": 0.65,
                    "verified": False,

                    "evidence": build_evidence(
                        segment
                    ),
                }
            )

            continue

        # -------------------------------------------------
        # ADD OBJECTS
        # -------------------------------------------------

        if (
            "multiple objects" in text_lower
            or "create multiple objects" in text_lower
        ):

            steps.append(
                {
                    "step": len(steps) + 1,
                    "action": "add_objects",
                    "name": None,
                    "path": None,
                    "instruction": text,
                    "start_time": segment[
                        "start_time"
                    ],
                    "end_time": segment[
                        "end_time"
                    ],

                    "confidence": 0.65,
                    "verified": False,

                    "evidence": build_evidence(
                        segment
                    ),
                }
            )

    return steps