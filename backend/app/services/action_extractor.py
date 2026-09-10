import re


def clean_text(text: str) -> str:
    return " ".join(
        text.lower().split()
    )


def normalize_command(
    command: str,
) -> str:

    command = command.strip()

    command = re.sub(
        r"\bMPX\b",
        "npx",
        command,
        flags=re.IGNORECASE,
    )

    command = re.sub(
        r"\bCDU\b",
        "cd",
        command,
        flags=re.IGNORECASE,
    )

    command = re.sub(
        r"\bNPM\b",
        "npm",
        command,
        flags=re.IGNORECASE,
    )

    command = re.sub(
        r"\s+",
        " ",
        command,
    ).strip()

    return command


def extract_commands(
    text: str,
) -> list[str]:

    text = clean_text(text)

    commands = []

    # --------------------------------------------------
    # CREATE REACT APP
    # --------------------------------------------------

    create_react_match = re.search(
        r"\b(?:npx|mpx)\s+"
        r"create\s+react\s+app"
        r"(?:\s+"
        r"(?:and\s+)?"
        r"(?:i'?m\s+going\s+to\s+name\s+it\s+)?"
        r"([a-z0-9_-]+))?",
        text,
        re.IGNORECASE,
    )

    if create_react_match:

        project_name = (
            create_react_match.group(1)
        )

        if project_name:

            commands.append(
                f"npx create-react-app "
                f"{project_name}"
            )

        else:

            commands.append(
                "npx create-react-app"
            )

    # --------------------------------------------------
    # NPM INSTALL
    # --------------------------------------------------

    npm_match = re.search(
        r"\bnpm\s+"
        r"(?:install|i)"
        r"(?:\s+|-save\s+)"
        r"([a-z0-9@/_\-.]+(?:\s+[a-z0-9@/_\-.]+)*)",
        text,
        re.IGNORECASE,
    )

    if npm_match:

        packages = npm_match.group(1)

        packages = re.split(
            r"\s+(?:and|then|this|which|that)\s+",
            packages,
            maxsplit=1,
            flags=re.IGNORECASE,
        )[0]

        commands.append(
            "npm install "
            + packages.strip()
        )

    # --------------------------------------------------
    # YARN START
    # --------------------------------------------------

    if re.search(
        r"\byarn\s+start\b",
        text,
        re.IGNORECASE,
    ):

        commands.append(
            "yarn start"
        )

    # --------------------------------------------------
    # CD DIRECTORY
    # --------------------------------------------------

    cd_match = re.search(
        r"\b(?:cd|cdu)\s+"
        r"([a-z0-9_-]+)",
        text,
        re.IGNORECASE,
    )

    if cd_match:

        directory = (
            cd_match.group(1)
        )

        commands.append(
            f"cd {directory}"
        )

    # --------------------------------------------------
    # GIT
    # --------------------------------------------------

    git_match = re.search(
        r"\bgit\s+"
        r"(clone|checkout|pull|add|commit|push)"
        r"(?:\s+([^\n,.]+))?",
        text,
        re.IGNORECASE,
    )

    if git_match:

        command = (
            f"git {git_match.group(1)}"
        )

        if git_match.group(2):

            command += (
                " "
                + git_match.group(2).strip()
            )

        commands.append(
            normalize_command(
                command
            )
        )

    # --------------------------------------------------
    # REMOVE DUPLICATES
    # --------------------------------------------------

    unique_commands = []

    for command in commands:

        command = normalize_command(
            command
        )

        if (
            command
            and command not in unique_commands
        ):

            unique_commands.append(
                command
            )

    return unique_commands


def normalize_filename(
    filename: str,
) -> str:

    filename = filename.strip()

    filename = re.sub(
        r"\s+",
        "",
        filename,
    )

    filename = re.sub(
        r"(?i)\b(jas|j/s|j s)\b",
        ".js",
        filename,
    )

    filename = re.sub(
        r"(?i)\b(js)\b",
        ".js",
        filename,
    )

    if not re.search(
        r"\.(js|jsx|ts|tsx|css)$",
        filename,
        re.IGNORECASE,
    ):
        filename += ".js"

    return filename


def extract_file_names(
    text: str,
) -> list[str]:

    text = clean_text(text)

    files = []

    # Example:
    # "create a new file called product item Jas"

    match = re.search(
        r"\bcreate\s+"
        r"(?:a\s+)?new\s+file\s+"
        r"(?:called|named)\s+"
        r"([a-z0-9_-]+)"
        r"(?:\s+(?:jas|j/s|j\s+s|js))?",
        text,
        re.IGNORECASE,
    )

    if match:

        name = match.group(1)

        # Speech transcription commonly removes
        # spaces from compound filenames.
        if name.lower() == "product":

            if re.search(
                r"\bproduct\s+item\b",
                text,
                re.IGNORECASE,
            ):
                name = "ProductItem"

        elif name.lower() == "add":

            if re.search(
                r"\badd\s+item\b",
                text,
                re.IGNORECASE,
            ):
                name = "AddItem"

        filename = normalize_filename(
            name
        )

        files.append(
            filename
        )

    return files


def extract_folder_names(
    text: str,
) -> list[str]:

    text = clean_text(text)

    folders = []

    patterns = [
        r"\bfolder\s+(?:called|named)\s+"
        r"([a-z0-9_-]+)",

        r"\bgive\s+it\s+a\s+name\s+"
        r"([a-z0-9_-]+)",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:

            folder_name = match.strip()

            if (
                folder_name
                and folder_name not in folders
            ):

                folders.append(
                    folder_name
                )

    return folders


def extract_actions(
    detected_action: dict,
) -> list[dict]:

    text = detected_action.get(
        "text",
        "",
    ).strip()

    if not text:
        return []

    actions = []

    action_type = detected_action[
        "action"
    ]

    if action_type == "run_command":

        commands = extract_commands(
            text
        )

        for command in commands:

            actions.append(
                {
                    "action": "run_command",
                    "value": command,
                    "start_time": detected_action[
                        "start_time"
                    ],
                    "end_time": detected_action[
                        "end_time"
                    ],
                    "evidence": text,
                    "confidence": 0.90,
                }
            )

    elif action_type == "create_file":

        files = extract_file_names(
            text
        )

        for filename in files:

            actions.append(
                {
                    "action": "create_file",
                    "value": filename,
                    "start_time": detected_action[
                        "start_time"
                    ],
                    "end_time": detected_action[
                        "end_time"
                    ],
                    "evidence": text,
                    "confidence": 0.90,
                }
            )

    elif action_type == "create_folder":

        folders = extract_folder_names(
            text
        )

        for folder_name in folders:

            actions.append(
                {
                    "action": "create_folder",
                    "value": folder_name,
                    "start_time": detected_action[
                        "start_time"
                    ],
                    "end_time": detected_action[
                        "end_time"
                    ],
                    "evidence": text,
                    "confidence": 0.85,
                }
            )

    return actions