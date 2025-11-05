from fractal_designer.IFS import IFS
from fractal_designer.shapes.square import Square

from fractal_designer.transformers.polygon_transformer import PolygonTransformer


class SierpinskiTriangle(PolygonTransformer):
    def __init__(self):
        super().__init__()
        self.polygons: list[Square] = [Square("r"), Square("g"), Square("b")]
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0, 0))
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0.25, 0.5))
        self.add_transformation(IFS(0.5, 0, 0, 0.5, 0.5, 0))
