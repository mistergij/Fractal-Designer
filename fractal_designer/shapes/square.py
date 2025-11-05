import numpy as np

from fractal_designer.custom_types import Float64NDArray


class Square:
    def __init__(self, color: str):
        self.color = color
        self.points: Float64NDArray = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T
