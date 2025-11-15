import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from shiny import reactive
from shiny.ui import card
from shiny.express import input, render, ui, output

num_transformations = reactive.value([])
transformations = reactive.value([])

with ui.sidebar():
    ui.input_action_button("add", "Add Transformation")
    ui.input_action_button("remove", "Remove Last Transformation")
    ui.input_action_button("replot", "Plot Transformations")
    ui.input_numeric("iterations", "Number of Iterations", 1, min=1, max=8)


@output
@render.plot(alt="A Fractal")
def plot():
    for i in range(len(num_transformations.get())):
        transformations.get().append(
            np.array(
                [
                    [input[f"a_{i}"](), input[f"b_{i}"](), input[f"e_{i}"]()],
                    [input[f"c_{i}"](), input[f"d_{i}"](), input[f"f_{i}"]()],
                    [0, 0, 1],
                ]
            )
        )

    points = reactive.value(np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T)

    old_points = [points.get()]
    new_points: list[np.typing.NDArray[np.float32]] = []
    colors = [(1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5)]

    for i in range(1, input.iterations() + 1):
        new_points = []
        for polygon in old_points:
            for transformation in transformations.get():
                new_points.append(transformation @ polygon)

        old_points = new_points

    fig, ax = plt.subplots() # pyright: ignore [reportUnknownMemberType]


    for i, w in enumerate(new_points):
        patch = Polygon(w[0:2, :].T, facecolor=colors[i % 3])
        ax.add_patch(patch)

    return fig


@reactive.effect
@reactive.event(input.add)
def add_transformation():
    i = reactive.value(len(num_transformations.get()))
    ui.insert_ui(
        card(
            ui.card_header(f"Transformation {i.get() + 1}"),
            ui.input_numeric(f"a_{i.get()}", "a", 1, min=-1, max=1, step=0.1),
            ui.input_numeric(f"b_{i.get()}", "b", 0, min=-1, max=1, step=0.1),
            ui.input_numeric(f"c_{i.get()}", "c", 0, min=-1, max=1, step=0.1),
            ui.input_numeric(f"d_{i.get()}", "d", 1, min=-1, max=1, step=0.1),
            ui.input_numeric(f"e_{i.get()}", "e", 0, min=-1, max=1, step=0.1),
            ui.input_numeric(f"f_{i.get()}", "f", 0, min=-1, max=1, step=0.1),
            ui.input_numeric(f"p_{i.get()}", "p", 0, min=-1, max=1, step=0.1),
            id=f"transformation_{i.get()}",
        ),
        selector="#add",
        where="beforeBegin",
    )
    num_transformations.get().append(0)


@reactive.effect
@reactive.event(input.remove)
def remove_transformation():
    ui.remove_ui(selector=".card:last")
    if num_transformations.get():
        num_transformations.get().pop()


@reactive.effect
@reactive.event(input.replot)
def replot_transformations():
    transformations.set([])
