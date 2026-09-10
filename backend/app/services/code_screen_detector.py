from __future__ import annotations


def detect_code_screen_window(
    action: dict,
    padding_seconds: float = 5.0,
) -> dict:
    """
    Build a focused coding-screen window around a developer action.

    The action is expected to contain:
        start_time
        end_time
        action
        value

    This does not inspect pixels yet.
    It simply identifies the most relevant video interval
    for later frame/code extraction.
    """

    start_time = float(action["start_time"])
    end_time = float(action["end_time"])

    window_start = max(
        start_time - padding_seconds,
        0.0,
    )

    window_end = (
        end_time + padding_seconds
    )

    return {
        "start_time": window_start,
        "end_time": window_end,
        "action": action.get("action"),
        "value": action.get("value"),
        "confidence": 0.90,
    }


def detect_code_screen_windows(
    actions: list[dict],
    padding_seconds: float = 5.0,
) -> list[dict]:
    """
    Build coding-screen windows for relevant developer actions.

    Currently focuses on:
        - create_file
        - edit_file

    Command actions are intentionally excluded because
    they are generally terminal-oriented rather than
    source-code editing windows.
    """

    if not actions:
        return []

    windows = []

    for action in actions:

        action_type = action.get("action")

        if action_type not in {
            "create_file",
            "edit_file",
        }:
            continue

        windows.append(
            detect_code_screen_window(
                action,
                padding_seconds=padding_seconds,
            )
        )

    windows.sort(
        key=lambda item: item["start_time"]
    )

    return windows