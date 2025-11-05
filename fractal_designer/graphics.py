from typing import override

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import QMenu

from fractal_designer.mixins.transformer import Transformer
from fractal_designer.windows.menu import MenuWindow
from fractal_designer.windows.fractal import FractalWindow


def add_actions(actions: list[QAction], menu: QMenu):
    for action in actions:
        menu.addAction(action)


class MainWindow(Transformer, MenuWindow):
    @override
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set title
        self.setWindowTitle("Transformations")

        self.fractal = FractalWindow()

        for name, action in self.actions.items():
            if name == "Exit":
                action.triggered.connect(self.close)
            elif name == "Fractal":
                action.triggered.connect(lambda checked: self.toggle_fractal(self.fractal))

    def toggle_fractal(self, window):
        window.hide() if self.fractal.isVisible() else window.show()
