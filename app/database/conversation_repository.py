from datetime import datetime
from uuid import uuid4

from app.database.collections import conversations


class ConversationRepository:

    def create(
        self,
        document_id: str,
        user_id: str | None = None,
        title: str = "New Chat",
    ):

        conversation = {
            "_id": str(uuid4()),
            "document_id": document_id,
            "user_id": user_id,
            "title": title,
            "created_at": datetime.utcnow(),
        }

        conversations.insert_one(conversation)

        return conversation

    def get(self, conversation_id: str):

        return conversations.find_one(
            {"_id": conversation_id}
        )

    # NEW
    def get_all(self):

        return list(
            conversations.find().sort(
                "created_at",
                -1,
            )
        )
    
    def update_title(self, conversation_id: str, title: str):

        result = conversations.update_one(
            {"_id": conversation_id},
            {"$set": {"title": title}},
        )

        return result.modified_count > 0