from app.parsers.router import parse_document
from app.processors.pipeline import process_document

from app.knowledge_units.pipeline import KnowledgePipeline

from app.embeddings.embedder import EmbeddingGenerator

from app.document_store.manager import DocumentStore

from app.database.document_repository import DocumentRepository
from app.database.knowledge_unit_repository import KnowledgeUnitRepository

from app.okf.extractor import OKFExtractor
from app.okf.storage import OKFStorage

from app.okf.section_builder import SectionBuilder
from app.okf.graph_merger import GraphMerger

from app.okf.schemas import OKFDocument


class DocumentPipeline:

    def __init__(self):

        self.document_repository = DocumentRepository()

        self.knowledge_repository = KnowledgeUnitRepository()

        self.knowledge_pipeline = KnowledgePipeline()

        self.embedder = EmbeddingGenerator()

        self.store = DocumentStore()

        # ----------------------------
        # OKF Components
        # ----------------------------

        self.okf_extractor = OKFExtractor()

        self.okf_storage = OKFStorage()

        self.section_builder = SectionBuilder()

        self.graph_merger = GraphMerger()

    def index_document(
        self,
        file_path: str,
    ):

        # ----------------------------
        # Parse Document
        # ----------------------------

        document = parse_document(file_path)

        document = process_document(document)

        # ----------------------------
        # Save Document
        # ----------------------------

        self.document_repository.create(document)

        # ----------------------------
        # Build Knowledge Units
        # ----------------------------

        knowledge_units = self.knowledge_pipeline.build(
            document
        )

        # ----------------------------
        # Save Knowledge Units
        # ----------------------------

        self.knowledge_repository.create_many(
            document.id,
            knowledge_units,
        )

        # ----------------------------
        # Build Sections
        # ----------------------------

        sections = self.section_builder.build(
            knowledge_units
        )

        # ----------------------------
        # Extract Graphs
        # ----------------------------

        graphs = []

        for section in sections:

            okf = self.okf_extractor.extract(
                document_id=document.id,
                chunk_text=section.content,
            )

            graphs.append(okf.graph)

        # ----------------------------
        # Merge Graphs
        # ----------------------------

        merged_graph = self.graph_merger.merge(
            graphs
        )

        # ----------------------------
        # Final OKF Document
        # ----------------------------

        okf_document = OKFDocument(
            document_id=document.id,
            graph=merged_graph,
        )

        # ----------------------------
        # Save OKF
        # ----------------------------

        self.okf_storage.save(
            okf_document
        )

        # ----------------------------
        # Generate Embeddings
        # ----------------------------

        embedded_units = self.embedder.embed(
            knowledge_units
        )

        # ----------------------------
        # Store in FAISS
        # ----------------------------

        self.store.vector_store.add(
            embedded_units
        )

        self.store.save()

        return document