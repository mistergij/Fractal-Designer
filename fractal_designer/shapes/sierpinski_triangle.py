import numpy as np

from custom_types import assert_transformation_shape
from fractal_designer.IFS import IFS
from shapes.square import Square

from fractal_designer.mixins.transformer import Transformer


class SierpinskiTriangle(Transformer):
    def __init__(self):
        super().__init__()
        self.polygons: list[Square] = [Square("r"), Square("g"), Square("b")]
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0, 0))
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0.25, 0.5))
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0.5, 0))
    
    def apply_transformation(self, shape_to_transform, iterations: int):
        polygon = assert_transformation_shape(shape_to_transform, (3, 4))
