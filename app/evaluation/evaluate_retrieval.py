from app.embeddings.embedder import generate_query_embeddings
from app.vectorstore.qdrant import search
import math

import json

DATASET_PATH = "/home/ruproy9924/important/InsightFlow/app/evaluation/manual_qdrant_evaluation_dataset.json"
    
def precision_at_k(relevant_nodes, retrieved_ids, k):
    retrieved = retrieved_ids[:k]
    
    if not retrieved:
        return 0.0
    
    relevant_retrieved = sum(
        node_id in relevant_nodes
        for node_id in retrieved
    )
    
    return relevant_retrieved / k

def recall_at_k(relevant_nodes, retrieved_ids, k):
    if not relevant_nodes:
        return 0.0
    retrieved = retrieved_ids[:k]
    
    if not retrieved:
        return 0.0
    
    relevant_retrieved = sum(
        node_id in relevant_nodes
        for node_id in retrieved)
    
    return relevant_retrieved / len(relevant_nodes)


def reciprocal_rank(relevant_nodes, retrieved_ids):
    for rank, node_id in enumerate(retrieved_ids, start = 1):
        if node_id in relevant_nodes:
            return 1.0/rank
    
    return 0.0


def ndcg_at_k(relevant_nodes, retrieved_ids, k):
    retrieved = retrieved_ids[:k]
    
    if not retrieved:
        return 0.0
    
    dcg = 0
    
    for rank, node_id in enumerate(retrieved, start=1):
        if node_id in relevant_nodes:
            dcg += 1 / math.log2(rank + 1)
            
    relevant_cnt = min(len(relevant_nodes), k)
    
    idcg = sum(
        1 / math.log2(rank+1)
        for rank in range(1,relevant_cnt + 1)
    )
    
    if idcg == 0:
        return 0.0
    
    return dcg / idcg

def evaluate():
    with open(DATASET_PATH, "r") as f:
        dataset = json.load(f)
        
    precision_scores = []
    recall_scores = []
    reciprocal_rank_scores = []
    ndcg_scores = []
    
    for item in dataset:
        query = item["query"]
        relevant_nodes = item["relevant_nodes"]
        
        query_embedding = generate_query_embeddings(query)
        
        results = search(query_embedding,top_k = 5)
        
        retrieved_ids = [str(result.id) for result in results]
        
        precision = precision_at_k(relevant_nodes, retrieved_ids, k=5)
        recall = recall_at_k(relevant_nodes, retrieved_ids, k=5)
        rr = reciprocal_rank(relevant_nodes, retrieved_ids)
        ndcg = ndcg_at_k(relevant_nodes, retrieved_ids, k=5)
        
        precision_scores.append(precision)
        recall_scores.append(recall)
        reciprocal_rank_scores.append(rr)   
        ndcg_scores.append(ndcg)
        
        total = len(dataset)

    print("=" * 80)
    print("BASELINE EVALUATION RESULTS")
    print("=" * 80)
        
        
    print(f"Queries: {total}\n")
    print()
        
    print(f"Precision@5: {sum(precision_scores)/total:.4f}")
    print(f"Recall@5: {sum(recall_scores)/total:.4f}")
    print(f"Reciprocal Rank: {sum(reciprocal_rank_scores)/total:.4f}")
    print(f"NDCG@5: {sum(ndcg_scores)/total:.4f}")
        
if __name__ == "__main__":
    evaluate()