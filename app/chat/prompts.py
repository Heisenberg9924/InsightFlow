"""
prompts.py

Prompt templates used by the InsightFlow AI chat system.
"""

# ---------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------

SYSTEM_PROMPT = """
You are InsightFlow AI.

You are an intelligent document understanding assistant.

Your job is to answer questions using ONLY the supplied context.

The supplied context consists of:

1. Knowledge Graph context
2. Retrieved document passages

Rules

1. Never invent information.


3. Prefer facts from the Knowledge Graph when available.

4. Use retrieved passages to provide supporting details.

5. Keep answers concise but complete.

6. Do not mention the retrieval process.

7. Do not mention embeddings or the knowledge graph.

8. If multiple facts support the answer, combine them naturally.
"""

# ---------------------------------------------------------------------
# User Prompt
# ---------------------------------------------------------------------

ANSWER_PROMPT = """
===============================
Knowledge Graph Context
===============================

{graph_context}

===============================
Retrieved Document Context
===============================

{vector_context}

===============================
Question
===============================

{question}

===============================
Answer
===============================
"""

# ---------------------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------------------


def build_answer_prompt(
    graph_context: str,
    vector_context: str,
    question: str,
) -> str:
    """
    Build the final prompt sent to the LLM.
    """

    return ANSWER_PROMPT.format(
        graph_context=graph_context.strip(),
        vector_context=vector_context.strip(),
        question=question.strip(),
    )