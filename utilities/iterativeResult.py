from dataclasses import dataclass
import numpy as np


@dataclass
class IterativeResult:
    solution: np.ndarray
    iterations: int
