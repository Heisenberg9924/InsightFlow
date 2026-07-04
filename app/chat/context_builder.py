"""
context_builder.py

Builds the final context that is sent to the LLM.
"""

from app.chat.prompts import (
    build_answer_prompt,
)


class ContextBuilder:
    """
    Combines multiple retrieval sources into
    a single LLM prompt.
    """

    def build(
        self,
        question: str,
        graph_context: str,
        vector_context: str,
    ) -> str:
        """
        Build the final prompt.
        """

        graph_context = self._clean(
            graph_context
        )

        vector_context = self._clean(
            vector_context
        )

        return build_answer_prompt(
            graph_context=graph_context,
            vector_context=vector_context,
            question=question,
        )

    # ----------------------------------------------------

    @staticmethod
    def _clean(
        text: str | None,
    ) -> str:
        """
        Clean retrieved context.
        """

        if text is None:
            return "No context available."

        text = text.strip()

        if not text:
            return "No context available."

        return text