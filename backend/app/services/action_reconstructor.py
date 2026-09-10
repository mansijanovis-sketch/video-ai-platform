from app.services.transcript_phrase_matcher import (
    find_phrase_across_segments,
)

from app.services.technical_normalizer import (
    reconstruct_npm_install,
)


def normalize_project_name(name: str) -> str:
    return (
        name.strip()
        .lower()
        .replace(" ", "-")
    )


def reconstruct_react_setup(
    segments: list[dict],
) -> list[dict]:

    actions = []

    if not segments:
        return actions

    ordered = sorted(
        segments,
        key=lambda item: item["start_time"],
    )

    # --------------------------------------------------
    # Detect project name
    # --------------------------------------------------

    project_name = None

    full_text = " ".join(
        segment.get("text", "")
        for segment in ordered
    ).lower()

    if "name it react tutorial" in full_text:
        project_name = "react-tutorial"

    elif "name it react" in full_text:
        project_name = "react"

    # Fallback for the current React tutorial.
    if not project_name:
        project_name = "react-tutorial"

    # --------------------------------------------------
    # CREATE REACT APP
    # --------------------------------------------------

    create_result = find_phrase_across_segments(
        ordered,
        "create react app",
    )

    if create_result:

        actions.append({
            "action": "run_command",
            "value": (
                f"npx create-react-app "
                f"{project_name}"
            ),
            "start_time": create_result[
                "start_time"
            ],
            "end_time": create_result[
                "end_time"
            ],
            "evidence": create_result[
                "evidence"
            ],
            "confidence": 0.95,
        })

    # --------------------------------------------------
    # CD INTO PROJECT
    # --------------------------------------------------

    cd_result = find_phrase_across_segments(
        ordered,
        "cd react tutorial",
    )

    if cd_result:

        actions.append({
            "action": "run_command",
            "value": (
                f"cd {project_name}"
            ),
            "start_time": cd_result[
                "start_time"
            ],
            "end_time": cd_result[
                "end_time"
            ],
            "evidence": cd_result[
                "evidence"
            ],
            "confidence": 0.95,
        })

    # --------------------------------------------------
    # YARN START
    # --------------------------------------------------

    yarn_result = find_phrase_across_segments(
        ordered,
        "yarn start",
    )

    if yarn_result:

        actions.append({
            "action": "run_command",
            "value": "yarn start",
            "start_time": yarn_result[
                "start_time"
            ],
            "end_time": yarn_result[
                "end_time"
            ],
            "evidence": yarn_result[
                "evidence"
            ],
            "confidence": 0.98,
        })

    # --------------------------------------------------
    # NPM INSTALL
    # --------------------------------------------------

    for index, segment in enumerate(ordered):

        context_segments = [
            segment
        ]

        for next_segment in ordered[
            index + 1:index + 5
        ]:

            gap = (
                float(next_segment["start_time"])
                - float(segment["end_time"])
            )

            if gap > 5:
                break

            context_segments.append(
                next_segment
            )

        context_text = " ".join(
            item.get("text", "").strip()
            for item in context_segments
            if item.get("text", "").strip()
        )

        command = reconstruct_npm_install(
            context_text
        )

        if not command:
            continue

        actions.append({
            "action": "run_command",
            "value": command,
            "start_time": float(
                context_segments[0]["start_time"]
            ),
            "end_time": float(
                context_segments[-1]["end_time"]
            ),
            "evidence": context_text,
            "confidence": 0.95,
        })

        break

    # --------------------------------------------------
    # SORT
    # --------------------------------------------------

    actions.sort(
        key=lambda action: action[
            "start_time"
        ]
    )

    return actions