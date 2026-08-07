from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, QueryResponse


client = QdrantClient(
    host = "localhost",
    port = 6333,
)

COLLECTION_NAME = "nodes"
VECTOR_SIZE = 1024

def create_collection():
    client.create_collection(
        collection_name= COLLECTION_NAME,
        vectors_config = VectorParams(
            size = VECTOR_SIZE,
            distance = Distance.COSINE,
        ),
    )
    
    

def ensure_collection():
    
    collections = client.get_collections()

    existing = {   #using set to make checking take place in O(1) instead of n.
     collection.name 
     for collection in collections.collections
   }

    if COLLECTION_NAME not in existing:
     create_collection()
     
     print(f"Collection '{COLLECTION_NAME}' created." )
    else:
     print(f"Collection '{COLLECTION_NAME}' already exists.")
     
def upsert_nodes(embedded_nodes):
    points = []
    for embedded_node in embedded_nodes:
        point = PointStruct(
            id=embedded_node.node.node_id,
            vector=embedded_node.embedding.tolist(),
            payload={
                "text" : embedded_node.node.text,
                "metadata" : embedded_node.node.metadata,
                },
        )
        points.append(point)
        
    result = client.upsert(
        collection_name = COLLECTION_NAME,
        points = points,
    )
    
    return result

def search(query_embedding, top_k=5):
    results = client.query_points(
        collection_name = COLLECTION_NAME,
        query = query_embedding.tolist(),
        limit = top_k,
        with_payload = True,
    )
    
    return results.points
    
    






    



