from typing import override

from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import QMenu

from fractal_designer.mixins.transformer import TransformerMixin
from fractal_designer.menu_window.menus import MenuWindow


def add_actions(actions: list[QAction], menu: QMenu):
    for action in actions:
        menu.addAction(action)


class MainWindow(TransformerMixin, MenuWindow):
    @override
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set title
        self.setWindowTitle("Transformations")
