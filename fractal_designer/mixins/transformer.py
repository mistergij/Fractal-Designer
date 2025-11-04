import numpy as np

from fractal_designer.IFS import IFS
from fractal_designer.types import assert_transformation_shape, Float64NDArray


class TransformerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transformation_matrices: list[Float64NDArray] = []

    def add_transformation(self, ifs: IFS):
        self.transformation_matrices.append(assert_transformation_shape(ifs.IFS, (3, 3)))
