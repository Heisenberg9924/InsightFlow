from pathlib import Path
from uuid import uuid4

import pandas as pd

from app.models.document import ParsedDocument, DocumentMetadata


def extract_excel_text(path: str) -> ParsedDocument:

    sheets = pd.read_excel(path, sheet_name=None)

    text = ""

    for sheet_name, df in sheets.items():
        text += f"\nSheet: {sheet_name}\n"
        text += df.to_string(index=False)
        text += "\n"

    metadata = DocumentMetadata(
        word_count=len(text.split()),
        sheet_names=list(sheets.keys())
    )

    return ParsedDocument(
        id=str(uuid4()),
        filename=Path(path).name,
        file_type="xlsx",
        text=text,
        metadata=metadata
    )