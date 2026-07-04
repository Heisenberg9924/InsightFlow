import re


def split_into_sections(text: str) -> list[str]:

    lines = text.splitlines()

    sections = []
    current = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Detect heading-like lines
        if (
            line.isupper()
            or line.endswith(":")
            or len(line.split()) <= 4
        ):

            if current:
                sections.append("\n".join(current))

            current = [line]

        else:

            current.append(line)

    if current:
        sections.append("\n".join(current))

    return sections