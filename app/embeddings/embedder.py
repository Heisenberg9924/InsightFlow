from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import numpy as np

from app.embeddings.models import EmbeddedNode


embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-large-en-v1.5"
    )

def generate_embeddings(nodes):
    embedded_nodes = []
    for node in nodes:
        embedding = np.array(embed_model.get_text_embedding(node.text), dtype = np.float32)
        embedded_nodes.append(
            EmbeddedNode(node=node, 
                         embedding=embedding,
                        )
        )
    return embedded_nodes

def generate_query_embeddings(query: str):
    return np.array(
        embed_model.get_text_embedding(query),
        dtype = np.float32,
    )

