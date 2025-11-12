import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from shiny import reactive
from shiny.ui import card
from shiny.express import input, render, ui

transformation_ids: dict[int: bool] = {0: False}

with ui.sidebar():
    with ui.card(id="transformation_0"):
        ui.card_header("Transformation 1")
        transformation_ids[0] = False
        ui.input_numeric("a_0", "a", 0.5, min=-1, max=1, step=0.1)
        ui.input_numeric("b_0", "b", 0, min=-1, max=1, step=0.1)
        ui.input_numeric("c_0", "c", 0, min=-1, max=1, step=0.1)
        ui.input_numeric("d_0", "d", 0.5, min=-1, max=1, step=0.1)
        ui.input_numeric("e_0", "e", 0, min=-1, max=1, step=0.1)
        ui.input_numeric("f_0", "f", 0, min=-1, max=1, step=0.1)
        ui.input_numeric("p_0", "p", 0, min=-1, max=1, step=0.1)
        ui.input_action_button("add_0", "Add Transformation")

    ui.input_numeric("iterations", "Number of Iterations", 1, min=1, max=8)

    # for id, added in transformation_ids.items():
    #     if not added:
    #         @reactive.effect
    #         @reactive.event(input[f"add_{id}"])
    #         def _():
    #             ui.insert_ui(
    #                 card(
    #                     ui.card_header(f"Transformation {id + 1}"),
    #                     ui.input_numeric(f"a_{id + 1}", "a", 1, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"b_{id + 1}", "b", 0, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"c_{id + 1}", "c", 0, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"d_{id + 1}", "d", 1, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"e_{id + 1}", "e", 0, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"f_{id + 1}", "f", 0, min=-1, max=1, step=0.1),
    #                     ui.input_numeric(f"p_{id + 1}", "p", 0, min=-1, max=1, step=0.1),
    #                     ui.input_action_button(f"add_{id + 1}", "Add Transformation"),
    #                     id=f"transformation_{id + 1}",
    #                 ),
    #                 selector=f"#transformation_{id}",
    #                 where="afterEnd",
    #             )
    #             transformation_ids[id] = True
    #             transformation_ids[id + 1] = False


@render.plot(alt="A Fractal")
def plot():
    transformations = []
    for i in transformation_ids:
        transformations.append(
            np.array(
                [
                    [input[f"a_{i}"](), input[f"b_{i}"](), input[f"e_{i}"]()],
                    [input[f"c_{i}"](), input[f"d_{i}"](), input[f"f_{i}"]()],
                    [0, 0, 1],
                ]
            )
        )

    points = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T

    old_points = [points]
    new_points = []
    colors = [(1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5)]

    for i in range(1, input.iterations() + 1):
        new_points = []
        for polygon in old_points:
            for transformation in transformations:
                new_points.append(transformation @ polygon)

        old_points = new_points

    fig, ax = plt.subplots()

    for i, w in enumerate(new_points):
        patch = Polygon(w[0:2, :].T, facecolor=colors[i % 3])
        ax.add_patch(patch)

    return fig
