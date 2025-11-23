"""
Program to interactively display and edit fractals. All python code was designed by Alexander Kral, with the
mathematical algorithm for random iteration adapted from "Fractals Everywhere" to enable specifying
probabilities (Barnsley, 1993, pp. 89-90). app.css and app.js were also designed by Alexander Kral, but
katex.css, katex.js, and auto-render.js are open-source libraries incorporated for aesthetic purposes.
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
            ui.head_content(
                ui.tags.script(
                    src="https://cdn.jsdelivr.net/npm/webfontloader@1.6.28/webfontloader.js",
                    integrity="sha256-4O4pS1SH31ZqrSO2A/2QJTVjTPqVe+jnYgOWUVr7EEc=",
                    crossorigin="anonymous",
                    defer = True
                ),
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
                    defer=True,
                ),
                ui.tags.script(
                    src="https://cdn.jsdelivr.net/npm/katex@0.16.25/dist/contrib/auto-render.min.js",
                    integrity="sha384-hCXGrW6PitJEwbkoStFjeJxv+fSOOQKOPbJxSfM6G5sWZjAyWhXiTIIAmQqnlLlh",
                    crossorigin="anonymous",
                    defer=True,
                ),
                ui.include_js("fractal_designer/js/app.js", defer=True),
                ui.include_css("fractal_designer/css/app.min.css"),
            ),
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

    min_transformation = -2.00
    max_transformation = 2.00

    @staticmethod
    @module.ui
    def transformation_card(
        transformation_num: int = 0,
        a: float = 0.50,
        b: float = 0,
        c: float = 0,
        d: float = 0.50,
        e: float = 0,
        f: float = 0,
        p: float = 0,
    ) -> ui.Tag:
        return ui.card(
            ui.div(f"Transformation {transformation_num}", class_="card-title"),
            ui.div(
                ui.div(
                    ui.input_numeric(
                        "a",
                        "a",
                        a,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-a",
                ),
                ui.div(
                    ui.input_numeric(
                        "b",
                        "b",
                        b,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-b",
                ),
                ui.div(
                    ui.input_numeric(
                        "c",
                        "c",
                        c,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-c",
                ),
                ui.div(
                    ui.input_numeric(
                        "d",
                        "d",
                        d,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-d",
                ),
                ui.div(
                    ui.input_numeric(
                        "e",
                        "e",
                        e,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-e",
                ),
                ui.div(
                    ui.input_numeric(
                        "f",
                        "f",
                        f,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
                    class_="input-f",
                ),
                ui.div(
                    ui.input_numeric(
                        "p",
                        "p",
                        p,
                        min=FractalDesigner.min_transformation,
                        max=FractalDesigner.max_transformation,
                        step=0.01,
                        update_on="blur",
                        width="10ch",
                    ),
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
        def compute_transformation() -> list[tuple[int, NDArrayFloat32]] | None:
            input.graph_transformations()

            _transformation_servers = self.transformation_servers.get()

            transformations: list[NDArrayFloat32] = []

            new_points: list[tuple[int, NDArrayFloat32]] = []

            def validate_value(name: str, value: float) -> float:
                if (value < FractalDesigner.min_transformation) or (value > FractalDesigner.max_transformation):
                    m = ui.modal(
                        f"Parameter {name} for Transformation {server_number} is invalid. Valid ranges are between {FractalDesigner.min_transformation} and {FractalDesigner.max_transformation}",
                        title="Range Error",
                        easy_close=True,
                    )
                    ui.modal_show(m)
                    raise ValueError(
                        f"Parameter {name} for Transformation {server_number} is invalid. Valid ranges are between {FractalDesigner.min_transformation} and {FractalDesigner.max_transformation}"
                    )
                return value

            for server_number, server in enumerate(_transformation_servers):
                try:
                    a = validate_value("a", server.get()[0]())
                    b = validate_value("b", server.get()[1]())
                    c = validate_value("c", server.get()[2]())
                    d = validate_value("d", server.get()[3]())
                    e = validate_value("e", server.get()[4]())
                    f = validate_value("f", server.get()[5]())
                except ValueError:
                    return

                transformations.append(
                    np.array(
                        [
                            [a, b, e],
                            [c, d, f],
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
                    try:
                        weights.append(validate_value("p", server.get()[6]()))
                    except ValueError:
                        return

                if np.sum(np.array(weights)) != 1:
                    m = ui.modal(
                        "Probabilities do not add up to one. Please check your input and try again.",
                        title="Probability Error",
                        easy_close=True,
                    )
                    ui.modal_show(m)
                    return

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
                layout_xaxis_tickmode="auto",
                layout_yaxis_range=[0, 1],
                layout_yaxis_tickmode="auto",
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

            if input.radio_mode.get() == "discrete" and new_points:
                # transformations_plotted: set[int] = set()

                indices: np.typing.NDArray[np.int32] = np.zeros([len(new_points)], dtype=np.int32)

                for i in range(_num_transformations):
                    polygon_points: list[NDArrayFloat32] = []

                    for j in range(i, len(new_points), _num_transformations):
                        polygon_points.append(new_points[j][1])

                    x_list_discrete: list[NDArrayFloat32 | None] = []
                    y_list_discrete: list[NDArrayFloat32 | None] = []

                    for polygon in polygon_points:
                        x_list_discrete.extend(polygon[0, :])
                        x_list_discrete.append(None)

                        y_list_discrete.extend(polygon[1, :])
                        y_list_discrete.append(None)

                    if x_list_discrete:
                        x_list_discrete.pop()

                    if y_list_discrete:
                        y_list_discrete.pop()

                    plot.widget.add_scatter(  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
                        x=x_list_discrete,
                        y=y_list_discrete,
                        fill="toself",
                        fillcolor=px.colors.qualitative.G10[i],
                        name=f"Transformation {i}",
                        legendgroup=f"Transformation {i}",
                        line_color=px.colors.qualitative.G10[i],
                    )

            elif input.radio_mode.get() == "continuous" and new_points:
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
                        self.transformation_card(f"transformation_{_num_transformations}", _num_transformations)
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
