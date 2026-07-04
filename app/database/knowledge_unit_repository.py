from datetime import datetime

from app.database.collections import knowledge_units
from app.knowledge_units.models import KnowledgeUnit


class KnowledgeUnitRepository:

    def create_many(
        self,
        document_id: str,
        units: list[KnowledgeUnit],
    ):

        records = []

        for unit in units:

            records.append(
                {
                    "_id": unit.id,
                    "document_id": document_id,
                    "title": unit.title,
                    "content": unit.content,
                    "created_at": datetime.utcnow(),
                }
            )

        if records:
            knowledge_units.insert_many(records)

    def get_by_document(
        self,
        document_id: str,
    ):

        return list(
            knowledge_units.find(
                {"document_id": document_id}
            )
        )