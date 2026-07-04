from dataclasses import dataclass, field
from typing import Any


@dataclass
class KnowledgeUnit:
    id: str
    title: str
    content: str

    metadata: dict[str, Any] = field(default_factory=dict)