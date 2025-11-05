from dataclasses import dataclass

import numpy as np

from fractal_designer.custom_types import Float64NDArray


@dataclass
class Square:
    color: str
    points: Float64NDArray = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T
