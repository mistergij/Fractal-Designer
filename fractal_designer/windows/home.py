from typing import override

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import QMenu

from fractal_designer.windows.matrix import MatrixWindow
from fractal_designer.windows.menu import MenuWindow
from fractal_designer.windows.fractal import FractalWindow


def add_actions(actions: list[QAction], menu: QMenu):
    for action in actions:
        menu.addAction(action)


class MainWindow(MenuWindow):
    @override
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set title
        self.setWindowTitle("Transformations")

        self.fractal = FractalWindow()
        self.matrix = MatrixWindow()

        for name, action in self.actions_dict.items():
            if name == "Exit":
                action.triggered.connect(self.close)
            elif name == "Fractal":
                action.triggered.connect(lambda checked: self.toggle_fractal(self.fractal))
            elif name == "Matrix":
                action.triggered.connect(lambda checked: self.toggle_matrix(self.matrix))

    def toggle_fractal(self, window):
        if self.fractal.isVisible():
            window.hide()
        else:
            window.show()
            window.activateWindow()
            window.raise_()

    def toggle_matrix(self, window):
        if self.matrix.isVisible():
            window.hide()
        else:
            window.show()
            window.activateWindow()
            window.raise_()
