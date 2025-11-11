from typing import override

from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtCore import QEvent
from PySide6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from fractal_designer.actions import Actions
from fractal_designer.windows.window import Window


class DesignWindow(Window, QMainWindow):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(actions, parent)

        self.setWindowTitle("Design")

        self.active_window = False

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        canvas = FigureCanvas(Figure())
        layout.addWidget(canvas)
        layout.addWidget(NavigationToolbar(canvas, self))

        self._ax = canvas.figure.subplots()

    @override
    def showEvent(self, event):
        super().showEvent(event)
        self.enable_all_actions("Design")

    @override
    def hideEvent(self, event):
        super().hideEvent(event)
        self.disable_all_actions("Design")
