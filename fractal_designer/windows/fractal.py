from typing import override

import numpy as np
from matplotlib.backends.backend_qt import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class FractalWindow(QMainWindow):
    @override
    def __init__(self, parent=None):
        super().__init__(parent)

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        static_canvas = FigureCanvas(Figure())
        layout.addWidget(static_canvas)
        layout.addWidget(NavigationToolbar(static_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self.setWindowTitle("Fractal")

        self.setMinimumSize(600, 600)
