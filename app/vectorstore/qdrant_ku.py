from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

import uuid


client = QdrantClient(
    host="localhost",
    port=6333,
)


COLLECTION_NAME = "knowledge_units"

VECTOR_SIZE = 1024


def create_collection():
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


def ensure_collection():

    collections = client.get_collections()

    existing = {
        collection.name
        for collection in collections.collections
    }

    if COLLECTION_NAME not in existing:

        create_collection()

        print(
            f"Collection '{COLLECTION_NAME}' created."
        )

    else:

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )


def upsert_knowledge_units(
    kus,
    embeddings,
    document_name,
):
    """
    Store Knowledge Units and their embeddings
    in Qdrant.
    """

    if len(kus) != len(embeddings):
        raise ValueError(
            "Number of KUs and embeddings must match."
        )

    points = []

    for ku, embedding in zip(kus, embeddings):

        point_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{document_name}:{ku.ku_id}",
            )
        )

        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "ku_id": ku.ku_id,
                "document": document_name,
                "text": ku.content,
                "context": ku.metadata.get("context"),
                "metadata": ku.metadata,
            },
        )

        points.append(point)

    result = client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return result


def search(
    query_embedding,
    top_k=5,
):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
        with_payload=True,
    )

    return results.points
