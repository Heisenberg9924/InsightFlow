"""
adapter.py

Converts OKF graphs into NetworkX graphs.
"""

import networkx as nx

from app.okf.schemas import KnowledgeGraph


class GraphAdapter:

    @staticmethod
    def to_networkx(
        graph: KnowledgeGraph,
    ) -> nx.MultiDiGraph:
        """
        Convert an OKF KnowledgeGraph into a NetworkX MultiDiGraph.
        """

        g = nx.MultiDiGraph()

        # --------------------------------------------------
        # Nodes
        # --------------------------------------------------

        for node in graph.nodes:

            g.add_node(
                node.id,
                label=node.label,
                properties=node.properties,
            )

        # --------------------------------------------------
        # Edges
        # --------------------------------------------------

        for edge in graph.edges:

            g.add_edge(
                edge.source,
                edge.target,
                key=edge.id,
                relation=edge.relation.value,
                properties=edge.properties,
            )

        return g

    # ------------------------------------------------------

    @staticmethod
    def get_node_label(
        graph: nx.MultiDiGraph,
        node_id: str,
    ) -> str:

        return graph.nodes[node_id].get(
            "label",
            "",
        )

    # ------------------------------------------------------

    @staticmethod
    def get_node_properties(
        graph: nx.MultiDiGraph,
        node_id: str,
    ):

        return graph.nodes[node_id].get(
            "properties",
            [],
        )