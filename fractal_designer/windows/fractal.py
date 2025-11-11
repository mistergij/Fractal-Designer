from typing import override

from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from fractal_designer.actions import Actions
from fractal_designer.shapes.sierpinski_triangle import SierpinskiTriangle
from fractal_designer.windows.window import Window


class FractalWindow(Window, QMainWindow):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(parent)

        self.actions_ = actions

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        canvas = FigureCanvas(Figure())
        layout.addWidget(canvas)
        layout.addWidget(NavigationToolbar(canvas, self))

        triangle = SierpinskiTriangle()
        triangle_points = triangle.apply_transformations(5)

        self._ax = canvas.figure.subplots()

        for w in triangle_points:
            for i, shape in enumerate(w):
                patch = Polygon(shape[0:2, :].T, facecolor=triangle.polygons[i % 3].color, edgecolor="k")
                self._ax.add_patch(patch)

        self.setWindowTitle("Fractal")

        self.setMinimumSize(600, 600)

        self.active_window = False

        # self.windowHandle().visibleChanged.connect(lambda: self.disable_all_actions("Fractal"))

    @override
    def showEvent(self, event):
        super().showEvent(event)
        self.enable_all_actions("Fractal")

    @override
    def hideEvent(self, event):
        super().hideEvent(event)
        self.disable_all_actions("Fractal")
