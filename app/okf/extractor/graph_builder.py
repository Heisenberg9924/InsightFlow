"""
graph_builder.py

Builds a KnowledgeGraph from parsed OKF data.
"""

from typing import Any
from uuid import uuid4

from app.okf.ontology import RelationType
from app.okf.schemas import (
    KnowledgeGraph,
    Node,
    Edge,
    Property,
)


class GraphBuilder:
    """
    Converts parsed JSON into a KnowledgeGraph.
    """

    def __init__(self):

        self.label_to_id: dict[str, str] = {}

        self.graph = KnowledgeGraph()

    # -----------------------------------------------------

    def build(
        self,
        parsed_data: dict[str, Any],
        source_chunk: str | None = None,
    ) -> KnowledgeGraph:
        """
        Build a KnowledgeGraph from parsed JSON.
        """

        self.graph = KnowledgeGraph()

        self.label_to_id.clear()

        # --------------------------------------------
        # Build Nodes
        # --------------------------------------------

        for node_data in parsed_data.get("nodes", []):

            node = self._build_node(
                node_data,
                source_chunk,
            )

            self.graph.nodes.append(node)

        # --------------------------------------------
        # Build Edges
        # --------------------------------------------

        for edge_data in parsed_data.get("edges", []):

            edge = self._build_edge(
                edge_data,
                source_chunk,
            )

            if edge is not None:
                self.graph.edges.append(edge)

        return self.graph

    # -----------------------------------------------------

    def _build_node(
        self,
        node_data: dict[str, Any],
        source_chunk: str | None,
    ) -> Node:

        label = node_data["label"].strip()

        # Avoid duplicate nodes
        if label in self.label_to_id:

            node_id = self.label_to_id[label]

            for node in self.graph.nodes:

                if node.id == node_id:
                    return node

        node_id = str(uuid4())

        self.label_to_id[label] = node_id

        properties = []

        for prop in node_data.get("properties", []):

            properties.append(
                Property(
                    key=prop["key"],
                    value=prop["value"],
                    confidence=prop.get(
                        "confidence",
                        1.0,
                    ),
                    source_chunk=source_chunk,
                )
            )

        return Node(
            id=node_id,
            label=label,
            properties=properties,
        )

    # -----------------------------------------------------

    def _create_missing_node(
        self,
        label: str,
    ) -> None:
        """
        Automatically create missing nodes referenced
        by Gemini relationships.
        """

        if label in self.label_to_id:
            return

        node = Node(
            id=str(uuid4()),
            label=label,
            properties=[],
        )

        self.label_to_id[label] = node.id

        self.graph.nodes.append(node)

        print(f"[OKF] Auto-created node: {label}")

    # -----------------------------------------------------

    def _build_edge(
        self,
        edge_data: dict[str, Any],
        source_chunk: str | None,
    ) -> Edge | None:

        source_label = edge_data["source"].strip()

        target_label = edge_data["target"].strip()

        # --------------------------------------------
        # Recover missing nodes instead of crashing
        # --------------------------------------------

        if source_label not in self.label_to_id:
            self._create_missing_node(source_label)

        if target_label not in self.label_to_id:
            self._create_missing_node(target_label)

        # --------------------------------------------
        # Edge Properties
        # --------------------------------------------

        properties = []

        for prop in edge_data.get("properties", []):

            properties.append(
                Property(
                    key=prop["key"],
                    value=prop["value"],
                    confidence=prop.get(
                        "confidence",
                        1.0,
                    ),
                    source_chunk=source_chunk,
                )
            )

        # --------------------------------------------
        # Relation Type
        # --------------------------------------------

        relation_value = edge_data.get(
            "relation",
            "RELATED_TO",
        ).strip().upper()

        try:

            relation = RelationType(relation_value)

        except ValueError:

            print(
                f"[OKF] Unknown relation '{relation_value}'. "
                "Using RELATED_TO."
            )

            relation = RelationType.RELATED_TO

        # --------------------------------------------
        # Create Edge
        # --------------------------------------------

        return Edge(

            source=self.label_to_id[source_label],

            relation=relation,

            target=self.label_to_id[target_label],

            properties=properties,
        )