from app.services.action_reconstructor import (
    reconstruct_react_setup,
)

from app.services.file_action_extractor import (
    extract_file_edit_actions,
)


def build_developer_action_timeline(
    segments: list[dict],
) -> list[dict]:
    """
    Combine command actions and file actions
    into one chronological developer-action timeline.
    """

    if not segments:
        return []

    command_actions = reconstruct_react_setup(
        segments
    )

    file_actions = extract_file_edit_actions(
        segments
    )

    actions = (
        command_actions
        + file_actions
    )

    actions.sort(
        key=lambda action: action["start_time"]
    )

    return actions