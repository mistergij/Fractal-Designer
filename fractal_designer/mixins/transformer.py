from fractal_designer.IFS import IFS
from fractal_designer.custom_types import assert_transformation_shape, Float64NDArray


class TransformerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transformation_matrices: list[Float64NDArray] = []
        self.polygons: list[Float64NDArray] = []

    def add_transformation(self, ifs: IFS):
        self.transformation_matrices.append(assert_transformation_shape(ifs.IFS, (3, 3)))
        
    def apply_polygon_transformation(self, polygon: Float64NDArray, iterations: int):
        polygon = assert_transformation_shape(polygon, (3, 4))
        old_polygons = [polygon]
        new_polygons = []
        
        for i in range(1, iterations):
            new_polygons = []
            for polygon in old_polygons:
                for transformation in self.transformation_matrices:
                    new_polygons.append(transformation @ polygon)
            
            old_polygons = new_polygons
        
        self.polygons = new_polygons
        