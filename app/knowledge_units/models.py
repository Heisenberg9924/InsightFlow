from dataclasses import dataclass, field


@dataclass
class KnowledgeUnit:
    ku_id: str
    parent_id: str
    content: str
    metadata: dict = field(default_factory=dict)