from pathlib import Path

from app.embeddings.vector_store import VectorStore


class DocumentStore:

    def __init__(
        self,
        storage_dir: str = "storage",
    ):

        self.storage_dir = Path(storage_dir)

        self.storage_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.vector_store = VectorStore()

    def save(self):

        self.vector_store.save(
            str(self.storage_dir)
        )

    def load(self):

        self.vector_store.load(
            str(self.storage_dir)
        )