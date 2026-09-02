from app.knowledge_units.models import KnowledgeUnit


def create_knowledge_units(
    text: str,
    parent_id: str,
    sentences: list[str],
    similarities: list[float],
    threshold: float,
    metadata: dict | None = None,
) -> list[KnowledgeUnit]:

    metadata = metadata or {}

    if not sentences:
        return []

    chunks = []
    current_chunk = [sentences[0]]

    for i, similarity in enumerate(similarities):

        next_sentence = sentences[i + 1]

        # Low similarity means a new semantic unit starts here.
        if similarity < threshold:

            chunks.append(
                " ".join(current_chunk)
            )

            current_chunk = [
                next_sentence
            ]

        else:

            current_chunk.append(
                next_sentence
            )

    # Add final chunk.
    chunks.append(
        " ".join(current_chunk)
    )

    knowledge_units = []

    for i, content in enumerate(chunks):

        knowledge_units.append(
            KnowledgeUnit(
                ku_id=f"{parent_id}_ku_{i}",
                parent_id=parent_id,
                content=content,
                metadata={
                    **metadata,
                    "parent_id": parent_id,
                },
            )
        )

    return knowledge_units