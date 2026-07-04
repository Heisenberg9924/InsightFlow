from sentence_transformers import SentenceTransformer
import numpy as np

from app.embeddings.models import EmbeddedKnowledgeUnit
from app.knowledge_units.models import KnowledgeUnit


class EmbeddingGenerator:

    _model = None

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):

        if EmbeddingGenerator._model is None:
            EmbeddingGenerator._model = SentenceTransformer(model_name)

        self.model = EmbeddingGenerator._model

    # ---------------------------------------------------------

    def embed(
        self,
        units: list[KnowledgeUnit]
    ) -> list[EmbeddedKnowledgeUnit]:

        embeddings = self.model.encode(
            [unit.content for unit in units],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return [
            EmbeddedKnowledgeUnit(
                knowledge_unit=unit,
                embedding=embedding,
            )
            for unit, embedding in zip(units, embeddings)
        ]

    # ---------------------------------------------------------

    def embed_query(
        self,
        query: str,
    ) -> np.ndarray:
        """
        Generate an embedding for a user query.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding.astype(np.float32)