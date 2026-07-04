from app.embeddings.vector_store import VectorStore

from app.llm.generator import GeminiGenerator
from app.llm.prompt_builder import PromptBuilder

from app.retrieval.retriever import Retriever


class RetrievalPipeline:

    def __init__(self, vector_store: VectorStore):

        self.retriever = Retriever(vector_store)

        self.generator = GeminiGenerator()

    def ask(
        self,
        question: str,
        history: list[dict],
    ) -> str:

        context = self.retriever.retrieve(question)

        prompt = PromptBuilder.build(
            question=question,
            context=context,
            history=history,
        )

        return self.generator.generate(prompt)