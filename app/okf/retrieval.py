"""
retrieval.py

Knowledge Graph retrieval for the Open Knowledge Format (OKF).
"""

import re
from collections import defaultdict
from typing import Dict, List, Set

import networkx as nx

from app.okf.storage import OKFStorage
from app.okf.schemas import (
    KnowledgeGraph,
)

from app.okf.adapter import GraphAdapter


class OKFRetriever:

    def __init__(self):

        self.storage = OKFStorage()

    # ---------------------------------------------------------

    def retrieve(
        self,
        document_id: str,
        question: str,
    ) -> str:
        """
        Retrieve graph context for a question.
        """

        okf = self.storage.get(document_id)

        if okf is None:
            return ""

        graph = okf.graph

        index = self._build_index(graph)

        matched_ids = self._find_matching_nodes(
            index,
            question,
        )

        if not matched_ids:
            return ""

        nx_graph = GraphAdapter.to_networkx(graph)

        return self._build_context(
            nx_graph,
            matched_ids,
        )

    # ---------------------------------------------------------

    def _build_index(
        self,
        graph: KnowledgeGraph,
    ) -> Dict[str, Set[str]]:

        index = defaultdict(set)

        for node in graph.nodes:

            for token in self._tokenize(node.label):
                index[token].add(node.id)

            for prop in node.properties:

                for token in self._tokenize(
                    str(prop.value)
                ):
                    index[token].add(node.id)

        return index

    # ---------------------------------------------------------

    def _find_matching_nodes(
        self,
        index: Dict[str, Set[str]],
        question: str,
    ) -> Set[str]:

        matched = set()

        for token in self._tokenize(question):

            matched.update(
                index.get(token, set())
            )

        return matched

    # ---------------------------------------------------------

    def _build_context(
        self,
        graph: nx.MultiDiGraph,
        matched_ids: Set[str],
    ) -> str:

        context = []

        visited = set()

        expanded = set()

        # ----------------------------------------
        # Expand one-hop neighbourhood
        # ----------------------------------------

        for node_id in matched_ids:

            if node_id not in graph:
                continue

            ego = nx.ego_graph(
                graph,
                node_id,
                radius=1,
                undirected=True,
            )

            expanded.update(ego.nodes())

        # ----------------------------------------
        # Node Information
        # ----------------------------------------

        context.append("Relevant Nodes:")
        context.append("")

        for node_id in expanded:

            if node_id in visited:
                continue

            visited.add(node_id)

            node = graph.nodes[node_id]

            context.append(
                f"Node: {node['label']}"
            )

            properties = node.get(
                "properties",
                [],
            )

            for prop in properties:

                context.append(
                    f"  - {prop.key}: {prop.value}"
                )

        # ----------------------------------------
        # Relationships
        # ----------------------------------------

        context.append("")
        context.append("Relationships:")
        context.append("")

        for source, target, data in graph.edges(
            data=True
        ):

            if (
                source not in expanded
                or target not in expanded
            ):
                continue

            source_label = graph.nodes[source][
                "label"
            ]

            target_label = graph.nodes[target][
                "label"
            ]

            relation = data["relation"]

            context.append(
                f"{source_label} --{relation}--> {target_label}"
            )

        return "\n".join(context)

    # ---------------------------------------------------------

    @staticmethod
    def _tokenize(
        text: str,
    ) -> List[str]:

        return re.findall(
            r"[a-zA-Z0-9_]+",
            text.lower(),
        )