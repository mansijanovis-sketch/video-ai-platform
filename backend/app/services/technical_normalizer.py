import re


def normalize_package_name(
    text: str,
) -> str | None:

    normalized = text.lower()

    # -----------------------------------------------
    # React Router DOM
    # -----------------------------------------------

    if (
        "react router dom"
        in normalized
        or "react-router-dom"
        in normalized
        or "reactor out or dom"
        in normalized
    ):

        return "react-router-dom"

    return None


def reconstruct_npm_install(
    text: str,
) -> str | None:

    normalized = text.lower()

    if "npm" not in normalized:
        return None

    if not re.search(
        r"\binstall\b|\bi\s*-\s*save\b",
        normalized,
    ):
        return None

    package = normalize_package_name(
        normalized
    )

    if not package:
        return None

    return (
        "npm install "
        f"{package}"
    )