"""
graph_merger.py
"""

import networkx as nx

from app.okf.schemas import (
    KnowledgeGraph,
)

from app.okf.adapter import GraphAdapter


class GraphMerger:

    def merge(
        self,
        graphs: list[KnowledgeGraph],
    ) -> KnowledgeGraph:

        merged = nx.compose_all(

            [
                GraphAdapter.to_networkx(g)
                for g in graphs
            ]
        )

        nodes = []
        edges = []

        # -------------------------
        # Nodes
        # -------------------------

        for node_id, data in merged.nodes(data=True):

            nodes.append(

                {
                    "id": node_id,
                    "label": data["label"],
                    "properties": data["properties"],
                }

            )

        # -------------------------
        # Edges
        # -------------------------

        for source, target, data in merged.edges(data=True):

            edges.append(

                {
                    "source": source,
                    "target": target,
                    "relation": data["relation"],
                    "properties": data["properties"],
                }

            )

        return KnowledgeGraph.model_validate(

            {
                "nodes": nodes,
                "edges": edges,
            }
        )