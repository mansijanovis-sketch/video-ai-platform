import re


ACTION_PATTERNS = {
    "run_command": [
        r"\bnpx\s+",
        r"\bnpm\s+(install|i|run|start|create)\b",
        r"\byarn\s+(start|install|add|build)\b",
        r"\bpnpm\s+(install|run|start|add)\b",
        r"\bcd\s+[A-Za-z0-9_./-]+",
        r"\bgit\s+(clone|checkout|pull|add|commit|push)\b",
        r"\bpip\s+install\b",
        r"\bpython\s+",
    ],

    "create_file": [
        r"\bcreate\s+(a\s+)?new\s+file\b",
        r"\bcreate\s+file\b",
        r"\bnew\s+file\b",
        r"\bfile\s+called\b",
        r"\bfile\s+named\b",
    ],

    "create_folder": [
        r"\bcreate\s+(a\s+)?new\s+folder\b",
        r"\bcreate\s+folder\b",
        r"\bnew\s+folder\b",
        r"\bcreate\s+(a\s+)?new\s+directory\b",
    ],
}


def detect_developer_actions(
    chunk: dict,
) -> list[dict]:

    text = chunk.get(
        "text",
        "",
    ).strip()

    if not text:
        return []

    actions = []

    for action_type, patterns in ACTION_PATTERNS.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):

                actions.append(
                    {
                        "action": action_type,
                        "start_time": chunk[
                            "start_time"
                        ],
                        "end_time": chunk[
                            "end_time"
                        ],
                        "text": text,
                        "confidence": 0.80,
                    }
                )

                break

    return actions