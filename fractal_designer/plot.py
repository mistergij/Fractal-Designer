import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

matplotlib.use('qtagg')

fig = plt.figure()
ax = fig.add_subplot()

matrix_1 = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]])
matrix_2 = np.array([[0.5, 0, 0], [0, 0.5, 0.5], [0, 0, 1]])
matrix_3 = np.array([[0.5, 0, 0.5], [0, 0.5, 0.5], [0, 0, 1]])

ifs = [matrix_1, matrix_2, matrix_3]

polygon = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T

old_polygons = [polygon]
new_polygons = []

for i in range(1, 10):
    new_polygons = []
    for polygon in old_polygons:
        for matrix in ifs:
            new_polygons.append(matrix @ polygon)
    
    old_polygons = new_polygons

for polygon in new_polygons:
    ax.add_patch(Polygon(polygon[0:2, :].T, closed=True))

plt.show()
