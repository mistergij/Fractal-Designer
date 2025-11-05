import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot()

matrix_1 = np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]])
matrix_2 = np.array([[0.5, 0, 0], [0, 0.5, 0.5], [0, 0, 1]])
matrix_3 = np.array([[0.5, 0, 0.5], [0, 0.5, 0.5], [0, 0, 1]])

ifs = [matrix_1, matrix_2, matrix_3]

bottom_left = np.array([0, 0, 1]).T
top_right = np.array([1, 1, 1]).T

past_lefts = [bottom_left]
past_rights = [top_right]
next_lefts = []
next_rights = []

for i in range(1, 6):
    next_lefts = []
    next_rights = []
    for point in past_lefts:
        for matrix in ifs:
            next_lefts.append(matrix @ point)

    for point in past_rights:
        for matrix in ifs:
            next_rights.append(matrix @ point)

    past_lefts = next_lefts
    past_rights = next_rights

sizes = []

for left, right in zip(next_lefts, next_rights):
    left = left[0:2]
    right = right[0:2]
    size = right - left
    ax.add_patch(plt.Rectangle(left, size[0], size[1]))

plt.show()
