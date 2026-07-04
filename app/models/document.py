from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentMetadata:
    author: str | None = None
    created_at: str | None = None

    page_count: int | None = None
    word_count: int | None = None

    sheet_names: list[str] = field(default_factory=list)

    headings: list[str] = field(default_factory=list)

    tables: int = 0

    language: str | None = None

    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParsedDocument:
    id: str
    filename: str
    file_type: str
    text: str
    metadata: DocumentMetadata