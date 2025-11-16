import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Polygon
from shiny import App, Inputs, Outputs, Session, module, reactive, render, ui


app_ui = ui.page_sidebar(
    ui.sidebar(
        # [create_transformation(f"transformation_{i}") for i in range(3)],
        ui.output_ui("create_transformation"),
        ui.input_numeric("iterations", "Number of Iterations", 1, min=1, max=8),
        ui.input_action_button("add_transformation", "Add Transformation"),
    ),
    ui.output_plot("plot"),
)

num_transformations: reactive.Value[int] = reactive.value(0)
transformation_servers: reactive.Value[list[reactive.Value[list[reactive.Value[float]]]]] = reactive.value([])


@module.ui
def transformation_card(transformation_num: int = 0) -> ui.Tag:
    return ui.card(
        ui.card_header(f"Transformation {transformation_num}"),
        ui.input_numeric("a", "a", 1, min=-1, max=1, step=0.1),
        ui.input_numeric("b", "b", 0, min=-1, max=1, step=0.1),
        ui.input_numeric("c", "c", 0, min=-1, max=1, step=0.1),
        ui.input_numeric("d", "d", 1, min=-1, max=1, step=0.1),
        ui.input_numeric("e", "e", 0, min=-1, max=1, step=0.1),
        ui.input_numeric("f", "f", 0, min=-1, max=1, step=0.1),
        ui.input_numeric("p", "p", 0, min=-1, max=1, step=0.1),
        id="transformation",
    )


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


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def compute_transformation():
        input.add_transformation()
        _transformation_servers = transformation_servers.get()
        transformations: list[np.typing.NDArray[np.float32]] = []

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

        points = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]]).T

        old_points = [points]
        new_points: list[np.typing.NDArray[np.float32]] = []

        for _ in range(1, input.iterations() + 1):
            new_points = []
            for polygon in old_points:
                for transformation in transformations:
                    new_points.append(transformation @ polygon)

                old_points = new_points

        return new_points

    @render.plot(alt="A fractal")
    def plot():
        new_points: list[np.typing.NDArray[np.float32]] = compute_transformation()
        colors = [(1, 0, 0, 0.5), (0, 1, 0, 0.5), (0, 0, 1, 0.5)]

        fig, ax = plt.subplots()  # pyright: ignore [reportUnknownMemberType]

        for i, w in enumerate(new_points):
            patch = Polygon(w[0:2, :].T, facecolor=colors[i % 3])
            ax.add_patch(patch)

        return fig

    @render.ui
    @reactive.event(input.add_transformation)
    def create_transformation():
        _num_transformations = num_transformations.get()
        transformation_cards = [transformation_card(f"transformation_{i}", i) for i in range(_num_transformations + 1)]
        num_transformations.set(_num_transformations + 1)

        return transformation_cards

    @reactive.effect
    def create_transformation_servers():
        _num_transformations = num_transformations.get()
        _transformation_servers = transformation_servers.get()
        if _num_transformations != 0 and _num_transformations < 8:
            _transformation_servers.append(transformation_server(f"transformation_{_num_transformations - 1}"))
            transformation_servers.set(_transformation_servers)


app = App(app_ui, server)
