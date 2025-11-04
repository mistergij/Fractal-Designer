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
from PySide6.QtWidgets import QMainWindow, QLabel

from fractal_designer.mixins.transformer import TransformerMixin


class FractalLabel(TransformerMixin, QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        min_height = 400
        min_width = 400

        self.setMinimumSize(min_width, min_height)


class FractalWindow(TransformerMixin, QMainWindow):
    @override
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Fractal")

        self.label = FractalLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        min_width = self.label.minimumWidth()
        min_height = self.label.minimumHeight()

        self.setMinimumSize(min_width+200, min_height+200)

        self.setCentralWidget(self.label)

        self.polygon = QPolygonF(
            [
                QPointF(50, 50),
                QPointF(50, min_height - 50),
                QPointF(min_width - 50, min_height - 50),
                QPointF(min_width - 50, 50),
                QPointF(50, 50),
            ]
        )

        self.path = QPainterPath()
        self.path.addPolygon(self.polygon)

        self.do_draw = True

        self.world_transform = QTransform()

        palette = self.palette()
        color = palette.color(QPalette.ColorRole.Window)

        self.pixmap = QPixmap(min_width, min_height)
        self.pixmap.fill(color)

    @override
    def paintEvent(self, event):
        painter = QPainter(self.pixmap)
        painter.setPen(QPen())
        painter.setBrush(QBrush())

        if self.do_draw:
            painter.drawPath(self.path)
            self.label.setPixmap(self.pixmap)


    @Slot()
    def draw(self):
        self.do_draw = True
        self.update()

    @Slot()
    def clear(self):
        self.do_draw = False
        self.update()
