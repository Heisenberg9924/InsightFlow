"""
section_builder.py

Builds semantic sections from Knowledge Units.
"""

from dataclasses import dataclass

from app.knowledge_units.models import KnowledgeUnit


@dataclass
class Section:
    title: str
    content: str


class SectionBuilder:

    def __init__(self, max_chars: int = 3500):
        self.max_chars = max_chars

    def build(
        self,
        knowledge_units: list[KnowledgeUnit],
    ) -> list[Section]:

        sections = []

        current_title = "Document"
        current_content = ""

        for unit in knowledge_units:

            block = f"""
Title:
{unit.title}

Content:
{unit.content}

----------------------------------------
"""

            if len(current_content) + len(block) > self.max_chars:

                sections.append(
                    Section(
                        title=current_title,
                        content=current_content.strip(),
                    )
                )

                current_content = block
                current_title = unit.title

            else:

                current_content += block

        if current_content:

            sections.append(
                Section(
                    title=current_title,
                    content=current_content.strip(),
                )
            )

        return sections