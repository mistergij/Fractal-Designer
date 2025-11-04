import numpy as np
from numpy.typing import NDArray


class IFS:
    def __init__(self, a: float = 1, b: float = 0, c: float = 0, d: float = 1, e: float = 0, f: float = 0):
        self.IFS = np.array([[a, b, e], [c, d, f], [0, 0, 1]])
