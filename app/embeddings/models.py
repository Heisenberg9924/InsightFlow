from dataclasses import dataclass

import numpy as np

from app.knowledge_units.models import KnowledgeUnit


@dataclass
class EmbeddedKnowledgeUnit:

    knowledge_unit: KnowledgeUnit

    embedding: np.ndarray