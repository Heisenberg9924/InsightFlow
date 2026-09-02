from app.embeddings.embedder import embed_model


def build_embedding_text(ku):
    """
    Construct the text that will be embedded.

    Structural context is included to improve retrieval,
    while the original KU content remains unchanged.
    """

    context = ku.metadata.get("context")

    if context:
        return f"{context}\n\n{ku.content}"

    return ku.content


def embed_knowledge_units(kus):
    """
    Generate one BGE embedding per Knowledge Unit.
    """

    embedding_texts = [
        build_embedding_text(ku)
        for ku in kus
    ]

    embeddings = [
        embed_model.get_text_embedding(text)
        for text in embedding_texts
    ]

    return embeddings