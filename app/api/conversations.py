from fastapi import APIRouter, HTTPException

from app.database.conversation_repository import ConversationRepository
from app.database.message_repository import MessageRepository

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)

conversation_repo = ConversationRepository()

message_repo = MessageRepository()


@router.get("")
def get_conversations():

    conversations = conversation_repo.get_all()

    return conversations


@router.get("/{conversation_id}")
def get_messages(conversation_id: str):

    conversation = conversation_repo.get(
        conversation_id
    )

    if conversation is None:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    messages = message_repo.get_messages(
        conversation_id
    )

    return {
        "conversation": conversation,
        "messages": messages
    }