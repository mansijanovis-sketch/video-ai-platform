import re


def normalize_text(
    text: str,
) -> str:

    text = text.lower()

    text = text.replace(
        "mpx",
        "npx",
    )

    text = text.replace(
        "cdu",
        "cd",
    )

    text = re.sub(
        r"[^a-z0-9\s_-]",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def build_context_text(
    segments: list[dict],
) -> str:

    return " ".join(
        segment.get(
            "text",
            "",
        ).strip()
        for segment in segments
        if segment.get(
            "text",
            "",
        ).strip()
    )


def find_phrase_across_segments(
    segments: list[dict],
    phrase: str,
    max_gap_seconds: float = 5.0,
) -> dict | None:

    if not segments:
        return None

    phrase_normalized = normalize_text(
        phrase
    )

    phrase_words = (
        phrase_normalized.split()
    )

    if not phrase_words:
        return None

    ordered = sorted(
        segments,
        key=lambda item: item[
            "start_time"
        ],
    )

    for index, segment in enumerate(
        ordered
    ):

        current_text = normalize_text(
            segment.get(
                "text",
                "",
            )
        )

        if not current_text:
            continue

        # --------------------------------------------------
        # Check whether this segment contains
        # the beginning of the requested phrase.
        # --------------------------------------------------

        first_word = phrase_words[0]

        if not re.search(
            rf"\b{re.escape(first_word)}\b",
            current_text,
        ):
            continue

        collected_segments = [
            segment
        ]

        collected_text = current_text

        start_time = float(
            segment["start_time"]
        )

        end_time = float(
            segment["end_time"]
        )

        # --------------------------------------------------
        # Check the current segment first.
        # --------------------------------------------------

        if phrase_normalized in collected_text:

            return {
                "phrase": phrase,
                "start_time": start_time,
                "end_time": end_time,
                "evidence": segment[
                    "text"
                ],
            }

        # --------------------------------------------------
        # Add nearby overlapping segments.
        # --------------------------------------------------

        for next_segment in ordered[
            index + 1:
        ]:

            next_start = float(
                next_segment["start_time"]
            )

            next_end = float(
                next_segment["end_time"]
            )

            # Stop when the next segment is
            # too far away.
            if (
                next_start
                - end_time
                > max_gap_seconds
            ):
                break

            next_text = normalize_text(
                next_segment.get(
                    "text",
                    "",
                )
            )

            if not next_text:
                continue

            collected_segments.append(
                next_segment
            )

            collected_text += (
                " "
                + next_text
            )

            end_time = max(
                end_time,
                next_end,
            )

            if (
                phrase_normalized
                in collected_text
            ):

                return {
                    "phrase": phrase,
                    "start_time": start_time,
                    "end_time": end_time,
                    "evidence": build_context_text(
                        collected_segments
                    ),
                }

    return None