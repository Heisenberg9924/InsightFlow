from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversation_router


app = FastAPI(
    title="InsightFlow AI",
)


app.include_router(
    health_router
)

app.include_router(
    upload_router
)

app.include_router(
    chat_router
)

app.include_router(
    conversation_router
)