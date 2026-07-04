from app.embeddings.models import EmbeddedKnowledgeUnit


class PromptBuilder:

    @staticmethod
    def build(
        question: str,
        context: list[EmbeddedKnowledgeUnit],
        history: list[dict],
    ) -> str:

        context_text = "\n\n".join(
            unit.knowledge_unit.content
            for unit in context
        )

        history_text = ""

        for msg in history:
            history_text += (
                f"{msg['role']}: {msg['content']}\n"
            )

        return f"""
You are InsightFlow AI.

Answer ONLY using the provided context.

If the answer is unavailable,
say so.

==========================
Conversation
==========================

{history_text}

==========================
Context
==========================

{context_text}

==========================
Question
==========================

{question}

==========================
Answer
==========================
"""