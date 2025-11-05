from typing import override

from fractal_designer.custom_types import assert_transformation_shape, Float64NDArray
from fractal_designer.transformers.transformer import Transformer
from fractal_designer.shapes.square import Square


class PolygonTransformer(Transformer):
    def __init__(self):
        super().__init__()

    @override
    def apply_transformation(self, shape_to_transform: Square, num_iterations: int) -> list[Float64NDArray]:
        polygon_points = assert_transformation_shape(shape_to_transform.points, (3, 4))

        old_points: list[Float64NDArray] = [polygon_points]
        new_points: list[Float64NDArray] = []

        for i in range(1, num_iterations + 1):
            new_points = []
            for polygon in old_points:
                for transformation in self.transformation_matrices:
                    new_points.append(transformation @ polygon)

            old_points = new_points

        return new_points
