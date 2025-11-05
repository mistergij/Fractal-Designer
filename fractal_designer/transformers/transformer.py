from abc import ABC, abstractmethod

from fractal_designer.IFS import IFS
from fractal_designer.custom_types import assert_transformation_shape, Float64NDArray


class Transformer(ABC):
    def __init__(self):
        self.transformation_matrices: list[Float64NDArray] = []
        self.polygons = []

    def add_transformation(self, ifs: IFS) -> None:
        ifs_array = assert_transformation_shape(ifs.IFS, (3, 3))
        self.transformation_matrices.append(ifs_array)

    @abstractmethod
    def apply_transformation(self, shape_to_transform, num_iterations: int) -> list[Float64NDArray]:
        raise NotImplementedError

    def apply_transformations(self, num_iterations: int) -> list[list[Float64NDArray]]:
        transformations: list[list[Float64NDArray]] = []
        for polygon in self.polygons:
            transformations.append(self.apply_transformation(polygon, num_iterations))

        return transformations
