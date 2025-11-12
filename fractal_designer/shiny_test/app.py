import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from shiny.express import input, render, ui

with ui.sidebar():
    with ui.card():
        ui.panel_title("Transformation 1")
        ui.input_numeric("a_0", "a", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("b_0", "b", 0, min=0, max=1, step=0.1)
        ui.input_numeric("c_0", "c", 0, min=0, max=1, step=0.1)
        ui.input_numeric("d_0", "d", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("e_0", "e", 0, min=0, max=1, step=0.1)
        ui.input_numeric("f_0", "f", 0, min=0, max=1, step=0.1)
        ui.input_numeric("p_0", "p", 0, min=0, max=1, step=0.1)

    with ui.card():
        ui.panel_title("Transformation 2")
        ui.input_numeric("a_1", "a", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("b_1", "b", 0, min=0, max=1, step=0.1)
        ui.input_numeric("c_1", "c", 0, min=0, max=1, step=0.1)
        ui.input_numeric("d_1", "d", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("e_1", "e", 0.25, min=0, max=1, step=0.1)
        ui.input_numeric("f_1", "f", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("p_1", "p", 0, min=0, max=1, step=0.1)

    with ui.card():
        ui.panel_title("Transformation 3")
        ui.input_numeric("a_2", "a", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("b_2", "b", 0, min=0, max=1, step=0.1)
        ui.input_numeric("c_2", "c", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("d_2", "d", 0, min=0, max=1, step=0.1)
        ui.input_numeric("e_2", "e", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("f_2", "f", 0.5, min=0, max=1, step=0.1)
        ui.input_numeric("p_2", "p", 0, min=0, max=1, step=0.1)

    ui.input_numeric("iterations", "Number of Iterations", 1, min=1, max=5)

@render.plot(alt="A Fractal")
def plot():
    transformations = []
    for i in range(3):
        transformations.append(np.array([[input[f"a_{i}"](), input[f"b_{i}"](), input[f"c_{i}"]()], [input[f"d_{i}"](), input[f"e_{i}"](), input[f"f_{i}"]()], [0, 0, 1]]))

    points = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T

    old_points = [points]
    new_points = []
    colors = ["r", "g", "b"]

    for i in range(1, input.iterations() + 1):
        new_points = []
        for polygon in old_points:
            for transformation in transformations:
                new_points.append(transformation @ polygon)
        
        old_points = new_points

    fig, ax = plt.subplots()

    for i, w in enumerate(new_points):
        patch = Polygon(w[0:2, :].T, facecolor=colors[i % 3], edgecolor = "k")
        ax.add_patch(patch)

    return fig
