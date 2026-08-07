SYSTEM_PROMPT = """
You are a helpful intelligent question-answering assistant.
Answer only using the provided context.

If the answer is not present in the context,
say that the information is not available in the context.

Rules:
1. Base your answers only on the provided context.
2. Do not hallucinate
3. Be concise and complete in your answers.
4. If multiple retrieved passages are relevant, combine them into a single coherent answer.

"""


def build_prompt(query: str, retrieved_nodes: list):
    
    context = "\n\n----------------------------\n\n".join(
        node.payload["text"] for node in retrieved_nodes
    )
    
    return f"""
    CONTEXT:
    {context}

    QUESTION:
    {query}
    
    ANSWER:
    """

