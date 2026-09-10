def build_action_context(
    segments: list[dict],
    action_start: float,
    action_end: float,
    padding_seconds: float = 15.0,
) -> list[dict]:

    context_start = max(
        action_start - padding_seconds,
        0,
    )

    context_end = (
        action_end + padding_seconds
    )

    context = []

    for segment in segments:

        start_time = float(
            segment["start_time"]
        )

        end_time = float(
            segment["end_time"]
        )

        if end_time < context_start:
            continue

        if start_time > context_end:
            continue

        context.append(
            {
                "start_time": start_time,
                "end_time": end_time,
                "text": segment.get(
                    "text",
                    "",
                ).strip(),
            }
        )

    return context


def combine_context_text(
    segments: list[dict],
) -> str:

    texts = []

    seen = set()

    for segment in segments:

        text = " ".join(
            segment.get(
                "text",
                "",
            ).split()
        )

        if not text:
            continue

        normalized = text.lower()

        if normalized in seen:
            continue

        seen.add(normalized)

        texts.append(text)

    return " ".join(texts)