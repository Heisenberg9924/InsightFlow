from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def home():

    return {
        "message": "InsightFlow AI is running!"
    }


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }