"""
validator.py

Validates a KnowledgeGraph before it is stored or used.
"""

from app.okf.schemas import KnowledgeGraph
from app.okf.ontology import RelationType
from app.okf.extractor.exceptions import GraphValidationError


class GraphValidator:
    """
    Validates the structural integrity of a KnowledgeGraph.
    """

    @staticmethod
    def validate(graph: KnowledgeGraph) -> None:
        """
        Raises GraphValidationError if the graph is invalid.
        """

        GraphValidator._validate_nodes(graph)
        GraphValidator._validate_edges(graph)

    # ---------------------------------------------------------

    @staticmethod
    def _validate_nodes(graph: KnowledgeGraph) -> None:
        """
        Validate graph nodes.
        """

        node_ids = set()
        node_labels = set()

        for node in graph.nodes:

            # Duplicate IDs
            if node.id in node_ids:
                raise GraphValidationError(
                    f"Duplicate node id '{node.id}'."
                )

            node_ids.add(node.id)

            # Empty label
            if not node.label.strip():
                raise GraphValidationError(
                    f"Node '{node.id}' has an empty label."
                )

            # Duplicate labels (V1 restriction)
            normalized_label = node.label.strip().lower()

            if normalized_label in node_labels:
                raise GraphValidationError(
                    f"Duplicate node label '{node.label}'."
                )

            node_labels.add(normalized_label)

    # ---------------------------------------------------------

    @staticmethod
    def _validate_edges(graph: KnowledgeGraph) -> None:
        """
        Validate graph edges.
        """

        node_ids = {node.id for node in graph.nodes}

        for edge in graph.edges:

            # Source exists
            if edge.source not in node_ids:
                raise GraphValidationError(
                    f"Edge source '{edge.source}' does not exist."
                )

            # Target exists
            if edge.target not in node_ids:
                raise GraphValidationError(
                    f"Edge target '{edge.target}' does not exist."
                )

            # Relation type
            if not isinstance(edge.relation, RelationType):
                raise GraphValidationError(
                    f"Invalid relation '{edge.relation}'."
                )

            # Prevent self-loops (optional)
            if edge.source == edge.target:
                raise GraphValidationError(
                    "Self-loop detected."
                )

            # Validate edge properties
            for prop in edge.properties:

                if not prop.key.strip():
                    raise GraphValidationError(
                        "Edge property has an empty key."
                    )

        # Validate node properties
        for node in graph.nodes:

            for prop in node.properties:

                if not prop.key.strip():
                    raise GraphValidationError(
                        f"Node '{node.label}' contains an empty property key."
                    )