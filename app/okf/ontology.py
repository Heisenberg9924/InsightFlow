"""
Open Knowledge Format (OKF) Ontology

This file defines the canonical ontology used throughout
InsightFlow AI.

DO NOT hardcode domain-specific concepts here.
The ontology should work for resumes, papers, contracts,
medical reports, legal documents, cybersecurity reports,
and every future document type.
"""

from enum import Enum


class RelationType(str, Enum):
    RELATED_TO = "RELATED_TO"

    HAS = "HAS"

    PART_OF = "PART_OF"

    USES = "USES"

    DEPENDS_ON = "DEPENDS_ON"

    CREATED_BY = "CREATED_BY"

    MENTIONS = "MENTIONS"

    REFERENCES = "REFERENCES"

    LOCATED_IN = "LOCATED_IN"

    CAUSES = "CAUSES"

    RESULTS_IN = "RESULTS_IN"