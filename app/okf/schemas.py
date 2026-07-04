"""
Open Knowledge Format (OKF) Schema

Canonical representation used by InsightFlow AI.

Everything extracted from every document is converted
into this format.
"""

from typing import Dict, List, Optional, Any
from uuid import uuid4

from pydantic import BaseModel, Field

from app.okf.ontology import RelationType

class Property(BaseModel):
    """
    Generic property for nodes and edges.
    """

    key: str

    value: Any
    
    confidence: float = 1.0
    
    source_chunk : str | None = None 


class Node(BaseModel):
    """
    Generic graph node.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    label: str

    properties: List[Property] = Field(default_factory=list)


class Edge(BaseModel):
    """
    Generic graph edge.
    """

    id: str = Field(default_factory=lambda: str(uuid4()))

    source: str

    relation: RelationType

    target: str

    properties: List[Property] = Field(default_factory=list)


class KnowledgeGraph(BaseModel):
    """
    Property Graph.
    """

    nodes: List[Node] = Field(default_factory=list)

    edges: List[Edge] = Field(default_factory=list)
    
    
class DocumentMetadata(BaseModel):
    """
    Generic metadata about the source document.
    """

    filename: Optional[str] = None

    title: Optional[str] = None

    source: Optional[str] = None

    author: Optional[str] = None

    created_at: Optional[str] = None

    language: Optional[str] = None


class OKFDocument(BaseModel):
    document_id: str

    graph: KnowledgeGraph

    metadata: DocumentMetadata = Field(
        default_factory=DocumentMetadata
    )

    summary: str | None = None