from uuid import uuid4

from app.knowledge_units.models import KnowledgeUnit
from app.knowledge_units.section_builder import Section


class KnowledgeUnitBuilder:

    def build(self, sections: list[Section]) -> list[KnowledgeUnit]:

        units = []

        for section in sections:

            units.append(
                KnowledgeUnit(
                    id=str(uuid4()),
                    title=section.title,
                    content=section.content,
                )
            )

        return units