from app.embeddings.embedder import generate_query_embeddings
from app.vectorstore.qdrant import search


def retrieve(query: str, top_k: int = 5):
    query_embedding = generate_query_embeddings(query)
    results = search(query_embedding=query_embedding, top_k=top_k)
    return results