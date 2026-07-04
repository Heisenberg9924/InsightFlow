import re
from dataclasses import dataclass

from app.models.document import ParsedDocument


@dataclass
class Section:
    title: str
    content: str


class SectionBuilder:
    """
    Detects logical sections from a ParsedDocument.

    Responsibilities:
    - Detect headings
    - Group related content under headings
    - Return ordered sections

    It DOES NOT:
    - Merge small sections
    - Split large sections
    - Count tokens
    """

    def __init__(self):
        self.heading_pattern = re.compile(r"^[A-Z][A-Z0-9\s&/\-]{2,}$")

    def _is_heading(self, line: str) -> bool:
        line = line.strip()

        if not line:
            return False

        # Markdown headings
        if line.startswith("#"):
            return True

        # ALL CAPS headings
        if self.heading_pattern.match(line):
            return True

        return False

    def build(self, document: ParsedDocument) -> list[Section]:

        lines = document.text.splitlines()

        sections = []

        current_title = "Introduction"
        current_content = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if self._is_heading(line):

                if current_content:
                    sections.append(
                        Section(
                            title=current_title,
                            content="\n".join(current_content).strip(),
                        )
                    )

                current_title = line
                current_content = []

            else:
                current_content.append(line)

        if current_content:
            sections.append(
                Section(
                    title=current_title,
                    content="\n".join(current_content).strip(),
                )
            )

        return sections