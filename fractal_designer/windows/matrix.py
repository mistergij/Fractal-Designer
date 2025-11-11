from typing import override

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QActionGroup

from fractal_designer.actions import Actions
from fractal_designer.widgets import MatrixInput, CompactInput
from fractal_designer.windows.window import Window


class InputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.current_layout = "Matrix Equation Form"

        self.transformation_list: list[QGroupBox] = []

        self.num_transformations = 0

        self.add_widget()

    def add_widget(self):
        widget: QGroupBox | None = None
        if self.current_layout == "Matrix Equation Form":
            widget = MatrixInput(self.num_transformations)
            self.transformation_list.append(widget)
        elif self.current_layout == "Compact Matrix Form":
            widget = CompactInput(self.num_transformations)
            self.transformation_list.append(widget)
        if widget is not None:
            self.layout().addWidget(widget)
            self.layout().addSpacing(20)
            self.num_transformations += 1

        if len(self.transformation_list) > 1:
            layout = self.transformation_list[-1].layout()
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda remove: self.remove_widget(len(self.transformation_list) - 1))

            if isinstance(layout, QGridLayout):
                if self.current_layout == "Matrix Equation Form":
                    layout.addWidget(remove_button, 0, 5, 2, 1)
                elif self.current_layout == "Compact Matrix Form":
                    layout.addWidget(remove_button, 1, 8, 1, 1)

    def remove_last_widget(self):
        self.remove_widget(len(self.transformation_list) - 1)

    def remove_widget(self, idx: int):
        widget: QGroupBox = self.transformation_list.pop(idx)
        self.layout().addSpacing(-20)
        self.num_transformations -= 1
        if idx < len(self.transformation_list) - 1:
            for i in range(idx, len(self.transformation_list)):
                self.transformation_list[i].setTitle(f"Transformation {i - 1}")
        widget.deleteLater()


class MatrixWindow(Window, QWidget):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(parent)
        self.actions_ = actions

        layout = QVBoxLayout(self)

        self.input_widget = InputWidget()

        layout.addWidget(self.input_widget)

        self.setWindowTitle("Matrix")

        self.active_window = False

        probabilities_group = QActionGroup(self)
        matrix_options_group = QActionGroup(self)

        for name, action in self.actions_.action_dicts["Matrix"].items():
            if name == "Calc. Probabilities":
                probabilities_group.addAction(action)
            elif name == "Auto Probabilities":
                probabilities_group.addAction(action)
            elif name == "Matrix Equation Form":
                matrix_options_group.addAction(action)
                action.triggered.connect(lambda _: self.set_mode(matrix_options_group))
            elif name == "Compact Matrix Form":
                matrix_options_group.addAction(action)
                action.triggered.connect(lambda _: self.set_mode(matrix_options_group))
            elif name == "Scale/Rotation Form":
                matrix_options_group.addAction(action)

    def set_mode(self, action_group: QActionGroup):
        checked_action_name = action_group.checkedAction().text()
        current_layout = self.input_widget.current_layout
        if current_layout != checked_action_name:
            self.input_widget.current_layout = checked_action_name
            while len(self.input_widget.transformation_list) != 0:
                self.input_widget.remove_last_widget()
            self.input_widget.add_widget()

    def add_transformation(self):
        self.input_widget.add_widget()

    @override
    def showEvent(self, event):
        super().showEvent(event)
        self.enable_all_actions("Matrix")

    @override
    def hideEvent(self, event):
        super().hideEvent(event)
        self.disable_all_actions("Matrix")
