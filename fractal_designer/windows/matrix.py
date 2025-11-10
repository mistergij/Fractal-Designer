from typing import cast, override

from PySide6.QtCore import QEvent, Qt, Signal, SignalInstance, Slot
from PySide6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QActionGroup

from fractal_designer.actions import Actions
from fractal_designer.widgets import MatrixInput, CompactInput


def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clear_layout(item.layout())


class MatrixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        matrix_layout = QVBoxLayout(self)

        matrix_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        matrix_input = MatrixInput()

        self.transformation_list = [matrix_input]

        matrix_layout.addWidget(matrix_input)
        matrix_layout.addSpacing(20)

    @override
    def changeEvent(self, event):
        if len(self.transformation_list) != 1:
            for i in self.transformation_list:
                layout = i.layout()
                remove_button = QPushButton("Remove")

                if isinstance(layout, QGridLayout):
                    layout.addWidget(remove_button, 0, 5, 2, 1)


class CompactWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        compact_layout = QVBoxLayout(self)

        compact_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        compact_input = CompactInput()

        self.transformation_list = [compact_input]

        compact_layout.addWidget(compact_input)
        compact_layout.addSpacing(20)

    @override
    def changeEvent(self, event):
        if len(self.transformation_list) != 1:
            for i in self.transformation_list:
                layout = i.layout()
                remove_button = QPushButton("Remove")

                if isinstance(layout, QGridLayout):
                    layout.addWidget(remove_button, 1, 8, 1, 1)


class MatrixWindow(QWidget):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(parent)
        self.actions_ = actions

        self.current_layout = "Matrix Equation Form"

        layout = QVBoxLayout(self)

        matrix_widget = MatrixWidget()

        layout.addWidget(matrix_widget)

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

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            self.active_window = not self.active_window
            if self.active_window:
                self.enable_all_actions("Matrix")
            else:
                self.disable_all_actions("Matrix")

    def disable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setDisabled(True)

    def enable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setEnabled(True)

    def set_mode(self, action_group: QActionGroup):
        checked_action_name = action_group.checkedAction().text()
        if self.current_layout != checked_action_name:
            clear_layout(self.layout())
            if checked_action_name == "Matrix Equation Form":
                self.layout().addWidget(MatrixWidget())
                self.current_layout = checked_action_name
            elif checked_action_name == "Compact Matrix Form":
                self.layout().addWidget(CompactWidget())
                self.current_layout = checked_action_name
