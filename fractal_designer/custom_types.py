import numpy as np
from numpy.typing import NDArray

Float64NDArray = NDArray[np.float64]


def assert_transformation_shape(array: Float64NDArray, shape: tuple[int, int]) -> Float64NDArray:
    assert array.shape == shape, "Shape does not match"
    return array
