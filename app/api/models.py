from pydantic import BaseModel


class ChatRequest(BaseModel):

    document_id: str

    question: str

    conversation_id: str | None = None


class ChatResponse(BaseModel):

    answer: str

    conversation_id: str


class UploadResponse(BaseModel):

    message: str

    filename: str

    document_id: str