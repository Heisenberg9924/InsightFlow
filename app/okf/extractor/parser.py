"""
parser.py

Parses and validates raw responses returned by Gemini.
"""

import json
import re
from typing import Any

from app.okf.extractor.exceptions import JSONParseError


class ResponseParser:
    """
    Parses and validates Gemini responses.
    """

    @staticmethod
    def clean_response(response: str) -> str:
        """
        Remove markdown fences and surrounding whitespace.
        """

        if not response:
            raise JSONParseError("Received an empty response.")

        response = response.strip()

        # Remove ```json
        response = re.sub(
            r"^```(?:json)?\s*",
            "",
            response,
            flags=re.IGNORECASE,
        )

        # Remove trailing ```
        response = re.sub(
            r"\s*```$",
            "",
            response,
        )

        return response.strip()

    @staticmethod
    def extract_json(response: str) -> str:
        """
        Extract the JSON object from a response.

        Handles cases where Gemini accidentally returns
        explanatory text before or after the JSON.
        """

        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            raise JSONParseError(
                "No JSON object found in Gemini response."
            )

        return response[start : end + 1]

    @classmethod
    def parse(cls, response: str) -> dict[str, Any]:
        """
        Convert Gemini response into a validated dictionary.
        """

        cleaned = cls.clean_response(response)

        json_string = cls.extract_json(cleaned)

        try:
            data = json.loads(json_string)

        except json.JSONDecodeError as e:
            raise JSONParseError(
                f"Invalid JSON returned by Gemini.\n{e}"
            )

        cls.validate(data)

        return data

    @staticmethod
    def validate(data: dict[str, Any]) -> None:
        """
        Validate the extracted JSON structure.
        """

        if not isinstance(data, dict):
            raise JSONParseError(
                "Top-level JSON object must be a dictionary."
            )

        if "nodes" not in data:
            raise JSONParseError(
                "Missing required field: 'nodes'."
            )

        if "edges" not in data:
            raise JSONParseError(
                "Missing required field: 'edges'."
            )

        if not isinstance(data["nodes"], list):
            raise JSONParseError(
                "'nodes' must be a list."
            )

        if not isinstance(data["edges"], list):
            raise JSONParseError(
                "'edges' must be a list."
            )

        # Validate nodes
        for index, node in enumerate(data["nodes"]):

            if not isinstance(node, dict):
                raise JSONParseError(
                    f"Node {index} is not a JSON object."
                )

            if "label" not in node:
                raise JSONParseError(
                    f"Node {index} is missing 'label'."
                )

            node.setdefault("properties", [])

            if not isinstance(node["properties"], list):
                raise JSONParseError(
                    f"Node {index} properties must be a list."
                )

        # Validate edges
        for index, edge in enumerate(data["edges"]):

            if not isinstance(edge, dict):
                raise JSONParseError(
                    f"Edge {index} is not a JSON object."
                )

            required_fields = [
                "source",
                "relation",
                "target",
            ]

            for field in required_fields:
                if field not in edge:
                    raise JSONParseError(
                        f"Edge {index} missing '{field}'."
                    )

            edge.setdefault("properties", [])

            if not isinstance(edge["properties"], list):
                raise JSONParseError(
                    f"Edge {index} properties must be a list."
                )