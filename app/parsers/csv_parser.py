from pathlib import Path
from uuid import uuid4

import pandas as pd

from app.models.document import ParsedDocument, DocumentMetadata


def extract_csv_text(path: str) -> ParsedDocument:

    df = pd.read_csv(path)

    text = df.to_string(index=False)

    metadata = DocumentMetadata(
        word_count=len(text.split()),
        extra={
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        }
    )

    return ParsedDocument(
        id=str(uuid4()),
        filename=Path(path).name,
        file_type="csv",
        text=text,
        metadata=metadata
    )