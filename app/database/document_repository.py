from datetime import datetime

from app.database.collections import documents
from app.models.document import ParsedDocument


class DocumentRepository:

    def create(self, document: ParsedDocument):

        record = {
            "_id": document.id,
            "filename": document.filename,
            "file_type": document.file_type,
            "metadata": document.metadata.__dict__,
            "uploaded_at": datetime.utcnow(),
        }

        documents.insert_one(record)

        return record

    def get(self, document_id: str):

        return documents.find_one(
            {"_id": document_id}
        )

    def get_all(self):

        return list(
            documents.find()
        )

    def delete(self, document_id: str):

        documents.delete_one(
            {"_id": document_id}
        )