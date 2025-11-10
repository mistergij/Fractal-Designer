from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Polygon
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from fractal_designer.actions import Actions
from fractal_designer.shapes.sierpinski_triangle import SierpinskiTriangle


class FractalWindow(QMainWindow):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(parent)
        
        self.actions_ = actions

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure())
        layout.addWidget(static_canvas)
        layout.addWidget(NavigationToolbar(static_canvas, self))

        triangle = SierpinskiTriangle()
        triangle_points = triangle.apply_transformations(5)

        self._static_ax = static_canvas.figure.subplots()

        for w in triangle_points:
            for i, shape in enumerate(w):
                patch = Polygon(shape[0:2, :].T, facecolor=triangle.polygons[i % 3].color, edgecolor="k")
                self._static_ax.add_patch(patch)

        self.setWindowTitle("Fractal")

        self.setMinimumSize(600, 600)
        
        self.active_window = False

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            self.active_window = not self.active_window
            if self.active_window:
                self.enable_all_actions("Fractal")
            else:
                self.disable_all_actions("Fractal")

    def disable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setDisabled(True)

    def enable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setEnabled(True)
