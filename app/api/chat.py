from fastapi import APIRouter, HTTPException

from app.api.models import ChatRequest, ChatResponse

from app.database.conversation_repository import ConversationRepository
from app.database.message_repository import MessageRepository

from app.document_store.manager import DocumentStore
from app.retrieval.pipeline import RetrievalPipeline


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

store = DocumentStore()
store.load()

pipeline = RetrievalPipeline(store.vector_store)

conversation_repo = ConversationRepository()
message_repo = MessageRepository()


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):

    conversation_id = request.conversation_id

    # ------------------------------------
    # Create new conversation if needed
    # ------------------------------------

    if conversation_id is None:

        conversation = conversation_repo.create(
            document_id=request.document_id,
        )

        conversation_id = conversation["_id"]

    else:

        conversation = conversation_repo.get(
            conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found.",
            )

    # ------------------------------------
    # Save user message
    # ------------------------------------

    message_repo.add_message(
        conversation_id,
        "user",
        request.question,
    )

    # ------------------------------------
    # Load updated conversation history
    # ------------------------------------

    history = message_repo.get_messages(
        conversation_id
    )

    # ------------------------------------
    # Generate response
    # ------------------------------------

    answer = pipeline.ask(
        request.question,
        history,
    )

    # ------------------------------------
    # Save assistant message
    # ------------------------------------

    message_repo.add_message(
        conversation_id,
        "assistant",
        answer,
    )
    
    if conversation["title"] == "New Chat":
        title = request.question.strip()
        if len(title) > 50:
            title = title[:50] + "..."
        conversation_repo.update_title(
            conversation_id,
            title,
        )

    # ------------------------------------
    # Return response
    # ------------------------------------

    return ChatResponse(
        answer=answer,
        conversation_id=conversation_id,
    )