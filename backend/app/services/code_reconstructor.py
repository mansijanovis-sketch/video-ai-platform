from __future__ import annotations

from difflib import SequenceMatcher


MATCH_THRESHOLD = 0.80


def normalize_line(line: str) -> str:
    """
    Normalize a source-code line for comparison only.
    """

    return " ".join(
        line.strip().lower().split()
    )


def line_similarity(
    first: str,
    second: str,
) -> float:
    """
    Calculate similarity between two source lines.
    """

    first_normalized = normalize_line(first)
    second_normalized = normalize_line(second)

    if not first_normalized or not second_normalized:
        return 0.0

    return SequenceMatcher(
        None,
        first_normalized,
        second_normalized,
    ).ratio()


def split_code_lines(
    code: str,
) -> list[str]:
    """
    Convert OCR output into non-empty source lines.
    """

    if not code:
        return []

    return [
        line.rstrip()
        for line in code.splitlines()
        if line.strip()
    ]


def align_lines(
    base_lines: list[dict],
    new_lines: list[str],
    threshold: float = MATCH_THRESHOLD,
) -> list[tuple]:
    """
    Align two ordered code sequences.

    Returns tuples:

        ("match", base_index, new_index, similarity)

        ("insert", None, new_index, 0.0)

    The alignment preserves source order.
    """

    if not base_lines:
        return [
            (
                "insert",
                None,
                index,
                0.0,
            )
            for index in range(len(new_lines))
        ]

    if not new_lines:
        return []

    base_text = [
        item["text"]
        for item in base_lines
    ]

    matcher = SequenceMatcher(
        a=[
            normalize_line(line)
            for line in base_text
        ],
        b=[
            normalize_line(line)
            for line in new_lines
        ],
        autojunk=False,
    )

    operations = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():

        if tag == "equal":

            for offset in range(i2 - i1):

                base_index = i1 + offset
                new_index = j1 + offset

                score = line_similarity(
                    base_text[base_index],
                    new_lines[new_index],
                )

                if score >= threshold:
                    operations.append(
                        (
                            "match",
                            base_index,
                            new_index,
                            score,
                        )
                    )
                else:
                    operations.append(
                        (
                            "insert",
                            None,
                            new_index,
                            0.0,
                        )
                    )

        elif tag in {"replace", "insert"}:

            for new_index in range(j1, j2):
                operations.append(
                    (
                        "insert",
                        None,
                        new_index,
                        0.0,
                    )
                )

    return operations


def merge_two_frames(
    base_lines: list[dict],
    new_lines: list[str],
    threshold: float = MATCH_THRESHOLD,
) -> list[dict]:
    """
    Merge a new OCR frame into the existing ordered source.

    Matching lines increase confidence.

    New lines are inserted according to sequence alignment.
    """

    if not base_lines:
        return [
            {
                "text": line,
                "confidence": 0.50,
                "observations": 1,
            }
            for line in new_lines
        ]

    if not new_lines:
        return base_lines

    alignment = align_lines(
        base_lines=base_lines,
        new_lines=new_lines,
        threshold=threshold,
    )

    matched_base_indices = set()

    # ---------------------------------------------------------
    # First update lines that matched.
    # ---------------------------------------------------------

    for operation in alignment:

        operation_type = operation[0]

        if operation_type != "match":
            continue

        base_index = operation[1]
        new_index = operation[2]
        score = operation[3]

        if base_index in matched_base_indices:
            continue

        matched_base_indices.add(
            base_index
        )

        item = base_lines[base_index]

        item["observations"] += 1

        item["confidence"] = min(
            1.0,
            (
                item["confidence"]
                + score
            )
            / 2.0,
        )

        # If the OCR line is more detailed/readable,
        # prefer the newer observation.
        if score >= 0.95:
            item["text"] = new_lines[
                new_index
            ]

    # ---------------------------------------------------------
    # Find new lines.
    # ---------------------------------------------------------

    insertions = []

    for operation in alignment:

        if operation[0] != "insert":
            continue

        new_index = operation[2]

        new_line = new_lines[
            new_index
        ]

        # -----------------------------------------------------
        # Find the nearest matched line BEFORE this new line.
        # -----------------------------------------------------

        previous_base_index = None

        for candidate in alignment:

            if candidate[0] != "match":
                continue

            candidate_new_index = candidate[2]

            if candidate_new_index < new_index:
                previous_base_index = candidate[1]

        # -----------------------------------------------------
        # Find the nearest matched line AFTER this new line.
        # -----------------------------------------------------

        next_base_index = None

        for candidate in alignment:

            if candidate[0] != "match":
                continue

            candidate_new_index = candidate[2]

            if candidate_new_index > new_index:
                next_base_index = candidate[1]
                break

        if previous_base_index is not None:

            position = (
                previous_base_index + 1
            )

        elif next_base_index is not None:

            position = next_base_index

        else:

            position = len(
                base_lines
            )

        insertions.append(
            {
                "position": position,
                "text": new_line,
            }
        )

    # ---------------------------------------------------------
    # Insert from bottom to top so positions remain stable.
    # ---------------------------------------------------------

    insertions.sort(
        key=lambda item: item["position"],
        reverse=True,
    )

    for insertion in insertions:

        position = max(
            0,
            min(
                insertion["position"],
                len(base_lines),
            ),
        )

        base_lines.insert(
            position,
            {
                "text": insertion["text"],
                "confidence": 0.50,
                "observations": 1,
            },
        )

    return base_lines


def reconstruct_code(
    frame_results: list[dict],
    threshold: float = MATCH_THRESHOLD,
) -> dict:
    """
    Reconstruct ordered source code from multiple
    timestamped OCR observations.
    """

    if not frame_results:
        return {
            "code": "",
            "lines": [],
        }

    ordered_frames = sorted(
        frame_results,
        key=lambda item: item.get(
            "timestamp",
            0.0,
        ),
    )

    first_lines = split_code_lines(
        ordered_frames[0].get(
            "code",
            "",
        )
    )

    reconstructed = [
        {
            "text": line,
            "confidence": 0.50,
            "observations": 1,
        }
        for line in first_lines
    ]

    for frame in ordered_frames[1:]:

        new_lines = split_code_lines(
            frame.get(
                "code",
                "",
            )
        )

        reconstructed = merge_two_frames(
            base_lines=reconstructed,
            new_lines=new_lines,
            threshold=threshold,
        )

    return {
        "code": "\n".join(
            item["text"]
            for item in reconstructed
        ),
        "lines": reconstructed,
    }