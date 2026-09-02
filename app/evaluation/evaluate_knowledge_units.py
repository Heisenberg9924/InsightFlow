from app.embeddings.embedder import generate_query_embeddings
from app.vectorstore.qdrant_ku import search

import json
import math


DATASET_PATH = (
    "/home/ruproy9924/important/InsightFlow/app/evaluation/final_qdrant_evaluation_dataset.json"
)


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
        for node_id in retrieved
    )

    return relevant_retrieved / len(relevant_nodes)


def reciprocal_rank(relevant_nodes, retrieved_ids):
    for rank, node_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if node_id in relevant_nodes:
            return 1.0 / rank

    return 0.0


def ndcg_at_k(relevant_nodes, retrieved_ids, k):
    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    dcg = 0.0

    for rank, node_id in enumerate(
        retrieved,
        start=1,
    ):
        if node_id in relevant_nodes:
            dcg += 1 / math.log2(rank + 1)

    relevant_count = min(
        len(relevant_nodes),
        k,
    )

    idcg = sum(
        1 / math.log2(rank + 1)
        for rank in range(
            1,
            relevant_count + 1,
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


def evaluate():

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        dataset = json.load(f)

    k_values = [1, 3, 5, 10]

    precision_scores = {
        k: []
        for k in k_values
    }

    recall_scores = {
        k: []
        for k in k_values
    }

    ndcg_scores = {
        k: []
        for k in k_values
    }

    reciprocal_rank_scores = []

    for index, item in enumerate(dataset, start=1):

        query = item["query"]

        relevant_nodes = set(
            item["relevant_nodes"]
        )

        query_embedding = (
            generate_query_embeddings(query)
        )

        results = search(
            query_embedding,
            top_k=10,
        )

        retrieved_ids = [
            str(result.id)
            for result in results
        ]

        for k in k_values:

            precision_scores[k].append(
                precision_at_k(
                    relevant_nodes,
                    retrieved_ids,
                    k,
                )
            )

            recall_scores[k].append(
                recall_at_k(
                    relevant_nodes,
                    retrieved_ids,
                    k,
                )
            )

            ndcg_scores[k].append(
                ndcg_at_k(
                    relevant_nodes,
                    retrieved_ids,
                    k,
                )
            )

        reciprocal_rank_scores.append(
            reciprocal_rank(
                relevant_nodes,
                retrieved_ids,
            )
        )

        first_match = next(
            (
                rank
                for rank, node_id
                in enumerate(
                    retrieved_ids,
                    start=1,
                )
                if node_id in relevant_nodes
            ),
            None,
        )

        print(
            f"[{index}/{len(dataset)}] "
            f"{item['id']} "
            f"→ first relevant rank: "
            f"{first_match}"
        )

    total = len(dataset)

    print()
    print("=" * 80)
    print("KNOWLEDGE UNIT EVALUATION RESULTS")
    print("=" * 80)

    print(f"Queries: {total}")
    print()

    for k in k_values:

        precision = (
            sum(precision_scores[k])
            / total
        )

        recall = (
            sum(recall_scores[k])
            / total
        )

        ndcg = (
            sum(ndcg_scores[k])
            / total
        )

        print(
            f"Precision@{k}: {precision:.4f}"
        )

        print(
            f"Recall@{k}:    {recall:.4f}"
        )

        print(
            f"NDCG@{k}:      {ndcg:.4f}"
        )

        print()

    mrr = (
        sum(reciprocal_rank_scores)
        / total
    )

    print(
        f"MRR:           {mrr:.4f}"
    )

    print("=" * 80)


if __name__ == "__main__":
    evaluate()