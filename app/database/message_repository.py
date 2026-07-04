from datetime import datetime
from uuid import uuid4

from app.database.collections import messages


class MessageRepository:

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):

        message = {
            "_id": str(uuid4()),
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
        }

        messages.insert_one(message)

    def get_messages(
        self,
        conversation_id: str,
    ):

        return list(
            messages.find(
                {"conversation_id": conversation_id}
            ).sort(
                "timestamp",
                1,
            )
        )