"""
query_engine.py

High-level query interface for the Open Knowledge Format (OKF).

Responsibilities
----------------
1. Receive a user query.
2. Retrieve relevant graph context.
3. Format the context for downstream consumers.
"""

from app.okf.retrieval import OKFRetriever


class OKFQueryEngine:

    """
    High-level interface over the graph retriever.

    Future versions can add:
    - multi-hop retrieval
    - graph ranking
    - graph reasoning
    - Cypher generation
    - graph summarization
    """

    def __init__(self):

        self.retriever = OKFRetriever()

    # -----------------------------------------------------

    def query(
        self,
        document_id: str,
        question: str,
    ) -> str:
        """
        Retrieve graph context relevant to a question.
        """

        context = self.retriever.retrieve(
            document_id=document_id,
            question=question,
        )

        if not context:

            return (
                "No relevant knowledge graph "
                "information found."
            )

        return self._format_context(context)

    # -----------------------------------------------------

    @staticmethod
    def _format_context(
        context: str,
    ) -> str:
        """
        Format retrieved graph context for an LLM.
        """

        return f"""
=========================
Knowledge Graph Context
=========================

{context}

=========================
End of Graph Context
=========================
""".strip()