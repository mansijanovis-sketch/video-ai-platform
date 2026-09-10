def chunk_transcript(
    segments: list[dict],
    max_chunk_seconds: float = 30.0,
) -> list[dict]:

    if not segments:
        return []

    sorted_segments = sorted(
        segments,
        key=lambda item: item["start_time"],
    )

    chunks = []

    current_start = None
    current_end = None
    current_texts = []

    seen_texts = set()

    for segment in sorted_segments:

        start_time = float(
            segment["start_time"]
        )

        end_time = float(
            segment["end_time"]
        )

        text = segment.get(
            "text",
            "",
        ).strip()

        if not text:
            continue

        if current_start is None:
            current_start = start_time
            current_end = end_time
            current_texts = []
            seen_texts = set()

        chunk_duration = (
            end_time - current_start
        )

        if (
            chunk_duration
            > max_chunk_seconds
            and current_texts
        ):
            chunks.append(
                {
                    "start_time": current_start,
                    "end_time": current_end,
                    "text": " ".join(
                        current_texts
                    ),
                }
            )

            current_start = start_time
            current_end = end_time
            current_texts = []
            seen_texts = set()

        normalized_text = " ".join(
            text.lower().split()
        )

        if normalized_text not in seen_texts:

            current_texts.append(text)

            seen_texts.add(
                normalized_text
            )

        current_end = max(
            current_end,
            end_time,
        )

    if current_texts:

        chunks.append(
            {
                "start_time": current_start,
                "end_time": current_end,
                "text": " ".join(
                    current_texts
                ),
            }
        )

    return chunks