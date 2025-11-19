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


class FractalDesigner:
    def __init__(self):
        self.app_ui = ui.page_sidebar(
            ui.sidebar(
                ui.output_ui("create_transformation"),
            ),
            output_widget("plot"),
            ui.input_radio_buttons("radio_mode", "Mode:", {"discrete": "Discrete", "continuous": "Continuous"}),
            ui.panel_conditional(
                "input.radio_mode === 'discrete'",
                ui.input_numeric("iterations_discrete", "Number of Iterations", 1, min=1, max=8, update_on="blur"),
            ),
            ui.panel_conditional(
                "input.radio_mode === 'continuous'",
                ui.input_numeric("iterations_continuous", "Number of Iterations", 1, min=1, max=5000, update_on="blur"),
            ),
            ui.input_action_button("add_transformation", "Add Transformation"),
            ui.input_action_button("graph_transformations", "Graph Transformations"),
        )

        self.num_transformations: reactive.Value[int] = reactive.value(0)
        self.transformation_servers: reactive.Value[list[reactive.Value[list[reactive.Value[float]]]]] = reactive.value(
            []
        )

    @staticmethod
    @module.ui
    def transformation_card(
        transformation_num: int = 0,
        a: float = 1,
        b: float = 0,
        c: float = 0,
        d: float = 1,
        e: float = 0,
        f: float = 0,
        p: float = 0,
    ) -> ui.Tag:
        return ui.card(
            ui.card_header(f"Transformation {transformation_num}"),
            ui.input_numeric("a", "a", a, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("b", "b", b, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("c", "c", c, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("d", "d", d, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("e", "e", e, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("f", "f", f, min=-2, max=2, step=0.1, update_on="blur"),
            ui.input_numeric("p", "p", p, min=-2, max=2, step=0.1, update_on="blur"),
            id="transformation",
        )

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
        def compute_transformation():
            input.graph_transformations()

            _transformation_servers = self.transformation_servers.get()
            transformations: list[np.typing.NDArray[np.float32]] = []
            new_points: list[np.typing.NDArray[np.float32]] = []

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
                old_points: list[np.typing.NDArray[np.float32]] = [
                    np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T
                ]

                for _ in range(input.iterations_discrete()):
                    new_points = []
                    for polygon in old_points:
                        for transformation in transformations:
                            new_points.append(transformation @ polygon)

                        old_points = new_points

            elif input.radio_mode.get() == "continuous" and transformations:
                point: np.typing.NDArray[np.float32] = np.array([0, 0, 1]).T
                weights: list[float] = []

                for server in _transformation_servers:
                    weights.append(server.get()[6]())

                if np.sum(np.array(weights)) != 1:
                    weights = [1 / len(weights) for _ in range(len(weights))]
                    m = ui.modal(
                        "Probabilities do not add up to one. Automatically corrected.",
                        title="Probability Error",
                        easy_close=True,
                    )
                    ui.modal_show(m)

                for _ in range(input.iterations_continuous()):
                    transformation = random.choices(transformations, weights=weights)
                    point = transformation @ point
                    point = point.T
                    new_points.append(point)

            return new_points

        @render_widget  # pyright: ignore [reportArgumentType]
        def plot():
            return go.Figure(
                layout_xaxis_range=[0, 1], layout_yaxis_range=[0, 1], layout_xaxis_dtick=0.1, layout_yaxis_dtick=0.1
            )

        @reactive.effect
        @reactive.event(input.graph_transformations)
        def _():
            new_points: list[np.typing.NDArray[np.float32]] = compute_transformation()
            plot.widget.data = []  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
            _num_transformations = self.num_transformations.get()

            if input.radio_mode.get() == "discrete":
                for i in range(_num_transformations):
                    polygon_points: list[np.typing.NDArray[np.float32]] = []
                    for j in range(i, len(new_points), _num_transformations):
                        polygon_points.append(new_points[j])

                    x_list_discrete: list[np.typing.NDArray[np.float32] | None] = []
                    y_list_discrete: list[np.typing.NDArray[np.float32] | None] = []
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
                        opacity=0.5,
                        name=f"Transformation {i}",
                    )

            elif input.radio_mode.get() == "continuous":
                scatter_points: list[np.typing.NDArray[np.float32]] = []

                for i in range(_num_transformations):
                    for j in range(i, len(new_points), _num_transformations):
                        scatter_points.append(new_points[j])

                    x_list_continuous: list[np.typing.NDArray[np.float32]] = []
                    y_list_continuous: list[np.typing.NDArray[np.float32]] = []

                    for scatter in scatter_points:
                        scatter = scatter.reshape([3, 1])  # Reshape into column vector
                        x_list_continuous.append(scatter[0, 0])  # First item in column vector
                        y_list_continuous.append(scatter[1, 0])  # Second item in column vector

                    # TODO: Implement proper color for continuous algorithm

                    plot.widget.add_scatter(  # pyright: ignore [reportOptionalMemberAccess, reportUnknownMemberType]
                        x=x_list_continuous,
                        y=y_list_continuous,
                        marker_color=px.colors.qualitative.G10[i],
                        name=f"Transformation {i}",
                        mode="markers",
                    )

        @render.ui
        @reactive.event(input.add_transformation)
        def create_transformation():
            _num_transformations = self.num_transformations.get()
            _transformation_servers = self.transformation_servers.get()

            transformation_cards: list[ui.Tag] = []

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
            return transformation_cards

        @reactive.effect
        def create_transformation_servers():
            _num_transformations = self.num_transformations.get()
            _transformation_servers = self.transformation_servers.get()
            if _num_transformations != 0 and _num_transformations < 8:
                _transformation_servers.append(
                    FractalDesigner.transformation_server(f"transformation_{_num_transformations - 1}")
                )
                self.transformation_servers.set(_transformation_servers)

    def get_server(self) -> Callable[[Inputs, Outputs, Session], None]:
        return self.server

    def get_ui(self) -> ui.Tag:
        return self.app_ui

designer = FractalDesigner()
app = App(designer.get_ui(), designer.get_server())
