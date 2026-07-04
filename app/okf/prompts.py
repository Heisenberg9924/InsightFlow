"""
prompts.py

Prompt templates for Open Knowledge Format (OKF) extraction.

This module ONLY contains prompts and prompt builders.

No API calls.
No parsing logic.
No validation logic.
"""

from app.okf.ontology import RelationType


# ==========================================================
# Allowed Relations
# ==========================================================

ALLOWED_RELATIONS = ", ".join(
    relation.value for relation in RelationType
)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are an Open Knowledge Format (OKF) Extraction Engine.

Your responsibility is to convert unstructured text into a
structured Open Knowledge Format (OKF).

The OKF represents knowledge using:

• Nodes
• Relationships
• Properties

You are NOT a chatbot.

You NEVER answer questions.

You NEVER explain your reasoning.

You NEVER summarize unless explicitly instructed.

You ONLY return structured knowledge.

============================================================

GENERAL RULES

1. Never invent information.

2. Every extracted node must be supported by the text.

3. Every extracted relationship must be supported by the text.

4. Never use external knowledge.

5. Never generate IDs or UUIDs.

6. Use concise canonical labels.

7. Prefer singular labels.

8. Remove duplicate nodes.

9. Return ONLY valid JSON.

10. Never return markdown.

11. Never include explanations.

============================================================

INTERNAL REASONING PROCESS

Perform the following steps internally.

DO NOT OUTPUT THESE STEPS.

Step 1
Identify all meaningful objects,
entities, concepts, events and values.

Step 2
Normalize labels.

If multiple labels refer to the same thing,
use one canonical label.

Step 3
Identify relationships between nodes.

Only create relationships explicitly
supported by the text.

Step 4
Extract useful properties for nodes
and relationships.

Step 5
Remove duplicate nodes.

Step 6
Validate every relationship.

Every edge must reference
existing nodes.

Step 7
Return ONLY valid JSON.
"""


# ==========================================================
# EXTRACTION PROMPT
# ==========================================================

EXTRACTION_PROMPT = """
Convert the following text into an Open Knowledge Format.

Extract:

1. Nodes

2. Relationships

3. Properties

------------------------------------------------------------

Each Node must contain

• label

• properties

------------------------------------------------------------

Each Relationship must contain

• source

• relation

• target

• properties

------------------------------------------------------------

Allowed Relations

{relations}

------------------------------------------------------------

STRICT RULES

• The value of "relation" MUST be exactly one of the allowed relations above.

• NEVER invent a new relation name.

• NEVER output relations such as:
  - BUILT_WITH
  - IMPLEMENTED_USING
  - HAS_SKILL
  - DEVELOPED_BY
  - WORKED_ON
  - CONTAINS
  - OWNS
  - INCLUDES

• If a relationship does not exactly match one of the allowed relations,
  use RELATED_TO.

• Every relation value MUST exactly match one of:
  {relations}

------------------------------------------------------------

TEXT

{text}
"""


# ==========================================================
# OUTPUT SCHEMA
# ==========================================================

OUTPUT_SCHEMA = """
Return ONLY valid JSON.

{
    "nodes": [
        {
            "label": "Node Label",
            "properties": [
                {
                    "key": "semantic_type",
                    "value": "Framework",
                    "confidence": 1.0
                }
            ]
        }
    ],

    "edges": [
        {
            "source": "Source Label",

            "relation": "USES",

            "target": "Target Label",

            "properties": [
                {
                    "key": "confidence",

                    "value": 1.0,

                    "confidence": 1.0
                }
            ]
        }
    ]
}
"""


# ==========================================================
# FEW SHOT EXAMPLE
# ==========================================================

EXAMPLE_OUTPUT = """
Example

Input Text

SafeDrive uses TensorFlow and CNN.
The system achieved 96% eye-state accuracy.

Expected Output

{
    "nodes":[
        {
            "label":"SafeDrive",
            "properties":[
                {
                    "key":"semantic_type",
                    "value":"Project",
                    "confidence":1.0
                }
            ]
        },
        {
            "label":"TensorFlow",
            "properties":[
                {
                    "key":"semantic_type",
                    "value":"Framework",
                    "confidence":1.0
                }
            ]
        },
        {
            "label":"CNN",
            "properties":[
                {
                    "key":"semantic_type",
                    "value":"Model",
                    "confidence":1.0
                }
            ]
        },
        {
            "label":"96%",
            "properties":[
                {
                    "key":"semantic_type",
                    "value":"Metric",
                    "confidence":1.0
                }
            ]
        }
    ],

    "edges":[
        {
            "source":"SafeDrive",
            "relation":"USES",
            "target":"TensorFlow",
            "properties":[]
        },
        {
            "source":"SafeDrive",
            "relation":"USES",
            "target":"CNN",
            "properties":[]
        },
        {
            "source":"SafeDrive",
            "relation":"HAS",
            "target":"96%",
            "properties":[
                {
                    "key":"metric_name",
                    "value":"Eye Accuracy",
                    "confidence":1.0
                }
            ]
        }
    ]
}
"""


# ==========================================================
# PROMPT BUILDER
# ==========================================================

def build_extraction_prompt(text: str) -> str:
    """
    Build the complete OKF extraction prompt.
    """

    return "\n\n".join(
        [
            SYSTEM_PROMPT,
            EXTRACTION_PROMPT.format(
                relations=ALLOWED_RELATIONS,
                text=text,
            ),
            OUTPUT_SCHEMA,
            EXAMPLE_OUTPUT,
        ]
    )