from dataclasses import dataclass

import numpy as np
from llama_index.core.schema import BaseNode


@dataclass
class EmbeddedNode:

    node : BaseNode

    embedding: np.ndarray