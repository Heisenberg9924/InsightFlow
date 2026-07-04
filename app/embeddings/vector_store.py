from pathlib import Path
import pickle

import faiss
import numpy as np

from app.embeddings.models import EmbeddedKnowledgeUnit


class VectorStore:

    def __init__(self, dimension: int = 384):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(dimension)

        self.knowledge_units: list[EmbeddedKnowledgeUnit] = []

    def add(self, units: list[EmbeddedKnowledgeUnit]) -> None:

        if not units:
            return

        vectors = np.vstack(
            [unit.embedding for unit in units]
        ).astype(np.float32)

        self.index.add(vectors)

        self.knowledge_units.extend(units)

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> list[EmbeddedKnowledgeUnit]:

        query = np.asarray(
            [query_embedding],
            dtype=np.float32,
        )

        _, indices = self.index.search(query, top_k)

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(
                self.knowledge_units[idx]
            )

        return results

    def save(self, directory: str) -> None:

        directory_path = Path(directory)

        directory_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Save FAISS index
        faiss.write_index(
            self.index,
            str(directory_path / "index.faiss"),
        )

        # Save metadata
        with open(
            directory_path / "knowledge_units.pkl",
            "wb",
        ) as f:

            pickle.dump(
                self.knowledge_units,
                f,
            )

    def load(self, directory: str) -> None:

        directory_path = Path(directory)

        # Load FAISS index
        self.index = faiss.read_index(
            str(directory_path / "index.faiss")
        )

        # Load knowledge units
        with open(
            directory_path / "knowledge_units.pkl",
            "rb",
        ) as f:

            self.knowledge_units = pickle.load(f)