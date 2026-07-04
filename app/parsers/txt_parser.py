from pathlib import Path
from uuid import uuid4

from app.models.document import ParsedDocument, DocumentMetadata


def extract_txt_text(path: str) -> ParsedDocument:

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    metadata = DocumentMetadata(
        word_count=len(text.split())
    )

    return ParsedDocument(
        id=str(uuid4()),
        filename=Path(path).name,
        file_type="txt",
        text=text,
        metadata=metadata
    )