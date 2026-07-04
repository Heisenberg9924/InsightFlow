from pathlib import Path
from uuid import uuid4

import fitz  # PyMuPDF

from app.models.document import ParsedDocument, DocumentMetadata


def extract_pdf_text(path: str) -> ParsedDocument:

    doc = fitz.open(path)

    text = ""

    for page in doc:
        page_text = str(page.get_text("text"))
        text += page_text + "\n"
        
    metadata_dict = doc.metadata or {}

    metadata = DocumentMetadata(
        author=metadata_dict.get("author"),
        page_count=doc.page_count,
        word_count=len(text.split())
    )

    return ParsedDocument(
        id=str(uuid4()),
        filename=Path(path).name,
        file_type="pdf",
        text=text,
        metadata=metadata
    )