from typing import cast, override

from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLineEdit,
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
        """
        Collects all input GroupBoxes and displays them properly
        :param QWidget parent: The Widget this instance is located in
        """
        super().__init__(parent)

        input_layout = QVBoxLayout(self)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.current_layout = "Matrix Equation Form"

        self.transformation_list: list[QGroupBox] = []

        self.num_transformations = 0

        self.add_widget()

    def add_widget(self) -> None:
        """
        Adds a single GroupBox to the layout depending on the active display form
        :return None
        """
        widget: QGroupBox | None = None
        if self.current_layout == "Matrix Equation Form":
            widget = MatrixInput(self.num_transformations)
            self.transformation_list.append(widget)
        elif self.current_layout == "Compact Matrix Form":
            widget = CompactInput(self.num_transformations)
            self.transformation_list.append(widget)
        if widget is not None:
            layout: QVBoxLayout = cast(QVBoxLayout, self.layout())
            layout.addWidget(widget)
            layout.addSpacing(20)
            self.num_transformations += 1

        if len(self.transformation_list) > 1:
            transformation_layout: QGridLayout = cast(QGridLayout, self.transformation_list[-1].layout())
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda remove: self.remove_widget(len(self.transformation_list) - 1))

            if isinstance(transformation_layout, QGridLayout):
                if self.current_layout == "Matrix Equation Form":
                    transformation_layout.addWidget(remove_button, 0, 5, 2, 1)
                elif self.current_layout == "Compact Matrix Form":
                    transformation_layout.addWidget(remove_button, 1, 8, 1, 1)

    def remove_last_widget(self) -> None:
        """
        Removes the last widget in transformation_list
        :return: None
        """
        self.remove_widget(len(self.transformation_list) - 1)

    def remove_widget(self, idx: int):
        """
        Removes an input GroupBox given its index
        :param idx: The index of the GroupBox in transformation_list
        :return: None
        """
        widget: QGroupBox = self.transformation_list.pop(idx)
        layout: QVBoxLayout = cast(QVBoxLayout, self.layout())
        layout.addSpacing(-20)
        self.num_transformations -= 1
        if idx < len(self.transformation_list) - 1:
            for i in range(idx, len(self.transformation_list)):
                self.transformation_list[i].setTitle(f"Transformation {i - 1}")
        widget.deleteLater()


class MatrixWindow(Window, QWidget):
    def __init__(self, actions: Actions, parent=None):
        """
        Creates the Matrix window to edit the current IFS
        :param Actions actions: The list of actions this window can perform
        :param QWidget parent: The Window this is located in, if applicable
        :returns: None
        """
        super().__init__(actions, parent)

        layout = QGridLayout(self)

        self.input_widget = InputWidget()

        layout.addWidget(self.input_widget, 0, 0, 1, 1)

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
