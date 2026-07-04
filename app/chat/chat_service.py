"""
chat_service.py

Main chat service for InsightFlow AI.

Pipeline

Question
    │
    ▼
Vector Retrieval
    │
    ▼
Knowledge Graph Retrieval
    │
    ▼
Context Builder
    │
    ▼
Gemini
    │
    ▼
Final Answer
"""

from app.chat.context_builder import ContextBuilder
from app.chat.llm import ChatLLM

from app.embeddings.embedder import EmbeddingGenerator

from app.document_store.manager import DocumentStore

from app.okf.query_engine import OKFQueryEngine


class ChatService:

    def __init__(self):

        # -----------------------------
        # Components
        # -----------------------------

        self.context_builder = ContextBuilder()

        self.llm = ChatLLM()

        self.embedder = EmbeddingGenerator()

        self.okf = OKFQueryEngine()

        self.store = DocumentStore()

        # Load FAISS index once
        self.store.load()

    # ---------------------------------------------------------

    def answer(
        self,
        document_id: str,
        question: str,
        top_k: int = 5,
    ) -> str:
        """
        Answer a question using both
        vector retrieval and knowledge graph retrieval.
        """

        # -----------------------------------------
        # Vector Retrieval
        # -----------------------------------------

        vector_context = self._retrieve_vector_context(
            question=question,
            top_k=top_k,
        )

        # -----------------------------------------
        # Knowledge Graph Retrieval
        # -----------------------------------------

        graph_context = self.okf.query(
            document_id=document_id,
            question=question,
        )

        # -----------------------------------------
        # Build Prompt
        # -----------------------------------------

        prompt = self.context_builder.build(
            question=question,
            graph_context=graph_context,
            vector_context=vector_context,
        )

        # -----------------------------------------
        # Generate Answer
        # -----------------------------------------

        return self.llm.generate(prompt)

    # ---------------------------------------------------------

    def _retrieve_vector_context(
        self,
        question: str,
        top_k: int,
    ) -> str:
        """
        Retrieve relevant passages using
        semantic similarity search.
        """

        query_embedding = self.embedder.embed_query(
            question
        )

        results = self.store.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        if not results:
            return ""

        passages = []

        for result in results:

            unit = result.knowledge_unit

            text = f"""
Title:
{unit.title}

Content:
{unit.content}
"""

            passages.append(
                text.strip()
            )

        return "\n\n".join(passages)