import os

from fastapi import APIRouter, UploadFile, File

from app.api.models import UploadResponse
from app.document_store.pipeline import DocumentPipeline


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


pipeline = DocumentPipeline()


@router.post(
    "",
    response_model=UploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
):

    filename = file.filename or "document"

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(file_path, "wb") as f:
        f.write(await file.read())

    pipeline.index_document(file_path)
    
    document = pipeline.index_document(file_path)

    return UploadResponse(
        message="Document uploaded successfully.",
        filename=document.filename,
        document_id=document.id,
    )