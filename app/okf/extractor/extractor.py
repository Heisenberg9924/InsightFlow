"""
Extract an OKF document from text.

The text may represent:
- a complete document
- a section
- or a single chunk
"""

from app.okf.schemas import (
    DocumentMetadata,
    KnowledgeGraph,
    OKFDocument,
)

from app.okf.extractor.llm import GeminiProvider
from app.okf.extractor.parser import ResponseParser
from app.okf.extractor.graph_builder import GraphBuilder
from app.okf.extractor.validator import GraphValidator


class OKFExtractor:
    """
    Main extraction engine.

    Pipeline

        Text
          │
          ▼
       Gemini
          │
          ▼
         JSON
          │
          ▼
        Parser
          │
          ▼
    Graph Builder
          │
          ▼
      Validator
          │
          ▼
      OKFDocument
    """

    def __init__(self):

        self.provider = GeminiProvider()
        self.parser = ResponseParser()
        self.validator = GraphValidator()

    # ---------------------------------------------------------

    def extract(
        self,
        document_id: str,
        chunk_text: str,
        chunk_id: str | None = None,
        metadata: DocumentMetadata | None = None,
    ) -> OKFDocument:
        """
        Extract an OKF document from a single chunk.
        """

        # -------------------------------------------------
        # Step 1: LLM Extraction
        # -------------------------------------------------

        raw_response = self.provider.generate(chunk_text)

        # -------------------------------------------------
        # Step 2: Parse JSON
        # -------------------------------------------------

        parsed = self.parser.parse(raw_response)

        # -------------------------------------------------
        # Step 3: Build Graph
        # -------------------------------------------------

        builder = GraphBuilder()

        graph: KnowledgeGraph = builder.build(
            parsed_data=parsed,
            source_chunk=chunk_id,
        )

        # -------------------------------------------------
        # Step 4: Validate Graph
        # -------------------------------------------------

        self.validator.validate(graph)

        # -------------------------------------------------
        # Step 5: Prepare Metadata
        # -------------------------------------------------

        document_metadata = (
            metadata if metadata is not None else DocumentMetadata()
        )

        # -------------------------------------------------
        # Step 6: Build OKF Document
        # -------------------------------------------------

        return OKFDocument(
            document_id=document_id,
            graph=graph,
            metadata=document_metadata,
            summary=None,
        )