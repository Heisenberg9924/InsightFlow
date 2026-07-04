"""
storage.py

Persistence layer for Open Knowledge Format (OKF).

Responsibilities
----------------
- Save OKF documents
- Retrieve OKF documents
- Delete OKF documents
- List stored OKF documents

This module contains NO retrieval logic.
"""

import os

from pymongo import MongoClient
from bson import ObjectId

from app.okf.schemas import OKFDocument


class OKFStorage:
    """
    MongoDB storage layer for OKF documents.
    """

    def __init__(self):

        mongo_uri = os.getenv(
            "MONGODB_URI",
            "mongodb://localhost:27017"
        )

        database_name = os.getenv(
            "MONGODB_DATABASE",
            "insightflow"
        )

        self.client = MongoClient(mongo_uri)

        self.db = self.client[database_name]

        self.collection = self.db["okf_documents"]

    # --------------------------------------------------

    def save(self, okf: OKFDocument) -> str:
        """
        Save an OKF document.

        Returns
        -------
        str
            MongoDB document id.
        """

        document = okf.model_dump()

        result = self.collection.insert_one(document)

        return str(result.inserted_id)

    # --------------------------------------------------

    def get(self, document_id: str) -> OKFDocument | None:
        """
        Retrieve an OKF document using the original document_id.
        """

        document = self.collection.find_one(
            {
                "document_id": document_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return OKFDocument(**document)

    # --------------------------------------------------

    def delete(self, document_id: str) -> bool:
        """
        Delete an OKF document.
        """

        result = self.collection.delete_one(
            {
                "document_id": document_id
            }
        )

        return result.deleted_count > 0

    # --------------------------------------------------

    def exists(self, document_id: str) -> bool:
        """
        Check whether an OKF document exists.
        """

        return (
            self.collection.count_documents(
                {
                    "document_id": document_id
                },
                limit=1,
            )
            > 0
        )

    # --------------------------------------------------

    def list_documents(self) -> list[str]:
        """
        Return all stored document ids.
        """

        cursor = self.collection.find(
            {},
            {
                "_id": 0,
                "document_id": 1,
            },
        )

        return [
            doc["document_id"]
            for doc in cursor
        ]

    # --------------------------------------------------

    def update(self, okf: OKFDocument) -> bool:
        """
        Replace an existing OKF document.
        """

        result = self.collection.replace_one(
            {
                "document_id": okf.document_id
            },
            okf.model_dump(),
        )

        return result.modified_count > 0
    
    def save_many(
    self,
    okf_documents: list[OKFDocument],
    ) -> None:

      if not okf_documents:
        return

      documents = [
        okf.model_dump()
        for okf in okf_documents
    ]

      self.collection.insert_many(documents)