"""
Program to interactively display and edit fractals. All code was designed by Alexander Kral, with the
mathematical algorithm for random iteration adapted from "Fractals Everywhere" to enable specifying
probabilities (Barnsley, 1993, pp. 89-90).
Author: Alexander Kral
"""

import random
from typing import Callable

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from shiny import App, Inputs, Outputs, Session, module, reactive, render, ui
from shinywidgets import output_widget, render_widget


NDArrayFloat32 = np.typing.NDArray[np.float32]


class FractalDesigner:
    def __init__(self):
        self.app_ui = ui.page_sidebar(
            ui.sidebar(
                ui.p(
                    """
                            $$
                                \\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} \\times
                                \\begin{bmatrix} x \\\\ y \\end{bmatrix} +
                                \\begin{bmatrix} e \\\\ f \\end{bmatrix}
                            $$
                        """
                ),
                ui.output_ui("create_transformation"),
                width=500,
            ),
            ui.tags.head(
                ui.tags.link(
                    rel="stylesheet",
                    href="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/katex.min.css",
                    integrity="sha384-WcoG4HRXMzYzfCgiyfrySxx90XSl2rxY5mnVY5TwtWE6KLrArNKn0T/mOgNL0Mmi",
                    crossorigin="anonymous",
                ),
                ui.tags.script(
                    src="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/katex.min.js",
                    integrity="sha384-J+9dG2KMoiR9hqcFao0IBLwxt6zpcyN68IgwzsCSkbreXUjmNVRhPFTssqdSGjwQ",
                    crossorigin="anonymous",
                ),
                ui.tags.script(
                    src="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/contrib/auto-render.min.js",
                    integrity="sha384-hCXGrW6PitJEwbkoStFjeJxv+fSOOQKOPbJxSfM6G5sWZjAyWhXiTIIAmQqnlLlh",
                    crossorigin="anonymous",
                ),
                ui.tags.script("""
                    document.addEventListener('DOMContentLoaded', function() {
                        renderMathInElement(document.body, {
                            delimiters: [
                                {left: "$$", right: "$$", display: true},
                                {left: "\\[", right: "\\]", display: true},
                                {left: "$", right: "$", display: false},
                                {left: "\\(", right: "\\)", display: false}
                            ]
                        });
                    });
                """),
            ),
            ui.head_content(ui.include_css("fractal_designer/app.css")),
            output_widget("plot").add_class("main-display"),
            ui.div(
                ui.input_radio_buttons("radio_mode", "Mode:", {"discrete": "Discrete", "continuous": "Continuous"}),
                class_="main-display",
            ),
            ui.panel_conditional(
                "input.radio_mode === 'discrete'",
                ui.input_numeric(
                    "iterations_discrete", "Number of Iterations:", 1, min=1, max=8, update_on="blur", width="20ch"
                ),
            ).add_class("main-display"),
            ui.panel_conditional(
                "input.radio_mode === 'continuous'",
                ui.input_numeric(
                    "iterations_continuous", "Number of Iterations:", 1, min=1, max=5000, update_on="blur", width="20ch"
                ),
            ).add_class("main-display"),
            ui.div(ui.input_action_button("add_transformation", "Add Transformation"), class_="main-display"),
            ui.div(
                ui.input_action_button("remove_transformation", "Remove Last Transformation"), class_="main-display"
            ),
            ui.div(
                ui.input_action_button("graph_transformations", "Graph Transformations").add_class("main-display"),
                class_="main-display",
            ),
        )

        self.num_transformations: reactive.Value[int] = reactive.value(0)
        self.transformation_servers: reactive.Value[list[reactive.Value[list[reactive.Value[float]]]]] = reactive.value(
            []
        )
        self.num_added = 0
        self.num_removed = 0

    @staticmethod
    @module.ui
    def transformation_card(
        transformation_num: int = 0,
        a: float = 0.5,
        b: float = 0,
        c: float = 0,
        d: float = 0.5,
        e: float = 0,
        f: float = 0,
        p: float = 0,
    ) -> ui.Tag:
        return ui.card(
            ui.div(f"Transformation {transformation_num}", class_="card-title"),
            ui.div(
                ui.div(
                    ui.input_numeric("a", "a", a, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-a",
                ),
                ui.div(
                    ui.input_numeric("b", "b", b, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-b",
                ),
                ui.div(
                    ui.input_numeric("c", "c", c, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-c",
                ),
                ui.div(
                    ui.input_numeric("d", "d", d, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-d",
                ),
                ui.div(
                    ui.input_numeric("e", "e", e, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-e",
                ),
                ui.div(
                    ui.input_numeric("f", "f", f, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-f",
                ),
                ui.div(
                    ui.input_numeric("p", "p", p, min=-2, max=2, step=0.01, update_on="blur", width="10ch"),
                    class_="input-p",
                ),
                class_="matrix",
            ),
            style="max-width: 25em",
            id="transformation",
        ).add_class("wrapper")

    @staticmethod
    @module.server
    def transformation_server(
        input: Inputs, output: Outputs, session: Session
    ) -> reactive.Value[list[reactive.Value[float]]]:
        transformation = reactive.value(
            [
                input.a,
                input.b,
                input.c,
                input.d,
                input.e,
                input.f,
                input.p,
            ]
        )

        return transformation

    def server(self, input: Inputs, output: Outputs, session: Session):
        @reactive.calc
        def compute_transformation() -> list[tuple[int, NDArrayFloat32]]:
            input.graph_transformations()

            _transformation_servers = self.transformation_servers.get()

            transformations: list[NDArrayFloat32] = []

            new_points: list[tuple[int, NDArrayFloat32]] = []

            for server in _transformation_servers:
                transformations.append(
                    np.array(
                        [
                            [server.get()[0](), server.get()[1](), server.get()[4]()],
                            [server.get()[2](), server.get()[3](), server.get()[5]()],
                            [0, 0, 1],
                        ]
                    )
                )

            if input.radio_mode.get() == "discrete":
                old_points: list[tuple[int, NDArrayFloat32]] = [
                    (0, np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T)
                ]

                for _ in range(input.iterations_discrete()):
                    new_points = []
                    for polygon in old_points:
                        for i, transformation in enumerate(transformations):
                            new_points.append((i, transformation @ polygon[1]))

                        old_points = new_points

            elif input.radio_mode.get() == "continuous" and transformations:
                point: NDArrayFloat32 = np.array([0, 0, 1]).T
                weights: list[float] = []

                for server in _transformation_servers:
                    weights.append(server.get()[6]())

                if np.sum(np.array(weights)) != 1:
                    weights = [1 / len(weights) for _ in range(len(weights))]
                    m = ui.modal(
                        "Probabilities adjusted to add up to one.",
                        title="Probability Error",
                        easy_close=True,
                    )
                    ui.modal_show(m)

                for _ in range(input.iterations_continuous()):
                    idx = range(len(transformations))
                    transformation_idx = random.choices(idx, weights=weights)[0]
                    transformation = transformations[transformation_idx]
                    point = transformation @ point
                    point = point.T
                    new_points.append((transformation_idx, point))

            return new_points

        @render_widget  # pyright: ignore [reportArgumentType]
        def plot():
            figure = go.Figure(
                layout_autosize=False,
                layout_width=500,
                layout_height=500,
                layout_xaxis_range=[0, 1],
                layout_xaxis_dtick=0.1,
                layout_yaxis_range=[0, 1],
                layout_yaxis_dtick=0.1,
                layout_xaxis_autorange=False,
                layout_yaxis_autorange=False,
                layout_legend_orientation="h",
            )
            # figure.update_layout(autosize=False, width=500, height=500, xaxis_range = [0, 1], yaxis_range = [0, 1], xaxis_autorange = False)
            # figure.update_yaxes(scaleanchor="x", scaleratio=1)
            return figure

        @reactive.effect
        @reactive.event(input.graph_transformations)
        def regraph_transformations():
            new_points = compute_transformation()
            plot.widget.data = []  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
            _num_transformations = self.num_transformations.get()

            if input.radio_mode.get() == "discrete":
                transformations_plotted: set[int] = set()

                for idx, transformation in new_points:
                    plot.widget.add_scatter(  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
                        x=transformation[0, :],
                        y=transformation[1, :],
                        fill="toself",
                        fillcolor=px.colors.qualitative.G10[idx],
                        name=f"Transformation {idx}",
                        legendgroup=f"Transformation {idx}",
                        showlegend=True if idx not in transformations_plotted else False,
                    )

                    transformations_plotted.add(idx)

            elif input.radio_mode.get() == "continuous":
                transformations_plotted: set[int] = set()
                x: NDArrayFloat32 = np.empty([len(new_points)], dtype=np.float32)
                y: NDArrayFloat32 = np.empty([len(new_points)], dtype=np.float32)
                indices: np.typing.NDArray[np.int32] = np.zeros([len(new_points)], dtype=np.int32)

                for i, (idx, transformation) in enumerate(new_points):
                    x[i] = transformation[0]
                    y[i] = transformation[1]
                    indices[i] = int(idx)

                unique_indices: set[int] = set(indices)

                for index in unique_indices:
                    plot.widget.add_scatter(  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
                        x=x[np.where(indices == index)],
                        y=y[np.where(indices == index)],
                        marker_color=px.colors.qualitative.G10[index],
                        name=f"Transformation {index}",
                        mode="markers",
                    )

        @render.ui
        @reactive.event(input.add_transformation, input.remove_transformation)
        def create_transformation():
            _num_transformations = self.num_transformations.get()
            _transformation_servers = self.transformation_servers.get()

            transformation_cards: list[ui.Tag] = []

            if input.remove_transformation() > self.num_removed:
                if _num_transformations > 0:
                    for i in range(_num_transformations - 1):
                        a = _transformation_servers[i].get()[0].get()
                        b = _transformation_servers[i].get()[1].get()
                        c = _transformation_servers[i].get()[2].get()
                        d = _transformation_servers[i].get()[3].get()
                        e = _transformation_servers[i].get()[4].get()
                        f = _transformation_servers[i].get()[5].get()
                        p = _transformation_servers[i].get()[6].get()
                        transformation_cards.append(
                            FractalDesigner.transformation_card(f"transformation_{i}", i, a, b, c, d, e, f, p)
                        )
                    remove_transformation_servers()
                    return transformation_cards
            elif input.add_transformation() > self.num_added:
                if _num_transformations == 0:
                    transformation_cards.append(FractalDesigner.transformation_card("transformation_0", 0))
                else:
                    for i in range(_num_transformations):
                        a = _transformation_servers[i].get()[0].get()
                        b = _transformation_servers[i].get()[1].get()
                        c = _transformation_servers[i].get()[2].get()
                        d = _transformation_servers[i].get()[3].get()
                        e = _transformation_servers[i].get()[4].get()
                        f = _transformation_servers[i].get()[5].get()
                        p = _transformation_servers[i].get()[6].get()
                        transformation_cards.append(
                            FractalDesigner.transformation_card(f"transformation_{i}", i, a, b, c, d, e, f, p)
                        )

                    transformation_cards.append(
                        FractalDesigner.transformation_card(f"transformation_{_num_transformations}", _num_transformations)
                    )

                self.num_transformations.set(_num_transformations + 1)
                create_transformation_servers()
                return transformation_cards

        @reactive.calc
        def create_transformation_servers():
            _num_transformations = self.num_transformations.get()
            _transformation_servers = self.transformation_servers.get()
            if _num_transformations != 0 and _num_transformations < 8:
                _transformation_servers.append(
                    FractalDesigner.transformation_server(f"transformation_{_num_transformations - 1}")
                )
                self.transformation_servers.set(_transformation_servers)
                self.num_added += 1

        @reactive.calc
        def remove_transformation_servers():
            _num_transformations = self.num_transformations.get()
            _transformation_servers = self.transformation_servers.get()
            if _num_transformations > 0:
                _transformation_servers.pop()
            self.transformation_servers.set(_transformation_servers)
            self.num_transformations.set(_num_transformations - 1)
            self.num_removed += 1

    def get_server(self) -> Callable[[Inputs, Outputs, Session], None]:
        return self.server

    def get_ui(self) -> ui.Tag:
        return self.app_ui


designer = FractalDesigner()
app = App(designer.get_ui(), designer.get_server())
