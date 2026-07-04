from app.embeddings.embedder import EmbeddingGenerator
from app.embeddings.vector_store import VectorStore
from app.embeddings.models import EmbeddedKnowledgeUnit


class Retriever:

    def __init__(self, vector_store: VectorStore):

        self.vector_store = vector_store
        self.embedder = EmbeddingGenerator()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[EmbeddedKnowledgeUnit]:

        query_embedding = self.embedder.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )