from typing import override

from PySide6.QtCore import QPointF, Qt, Slot
from PySide6.QtGui import (
    QBrush,
    QPainter,
    QPainterPath,
    QPalette,
    QPen,
    QPixmap,
    QPolygonF,
    QTransform,
)
from PySide6.QtWidgets import QGridLayout, QLabel, QMainWindow, QWidget

from fractal_designer.mixins.transformer import TransformerMixin


class MatrixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QGridLayout()


class MatrixWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
