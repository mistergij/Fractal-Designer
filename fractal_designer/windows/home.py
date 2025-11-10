import sys
from typing import override

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMenu

from actions import Actions
from fractal_designer.windows.fractal import FractalWindow
from fractal_designer.windows.matrix import MatrixWindow


class MainWindow(QMainWindow):
    def __init__(self, actions: Actions, parent=None):
        super().__init__(parent)
        self.actions_ = actions

        # Set title
        self.setWindowTitle("Transformations")

        self.create_menus()

        self.fractal_window = FractalWindow(self.actions_)
        self.matrix_window = MatrixWindow(self.actions_)

        for name, action in self.actions_.action_dicts["Window"].items():
            if name == "Exit":
                action.triggered.connect(self.close)
            elif name == "Fractal":
                action.triggered.connect(lambda checked: self.toggle_window(self.fractal_window))
            elif name == "Matrix":
                action.triggered.connect(lambda checked: self.toggle_window(self.matrix_window))

        for action in self.actions_.action_dicts["Matrix"].values():
            action.setDisabled(True)

    def create_menus(self):
        major_menu_names: list[str] = ["File", "Edit", "Matrix", "Design", "Fractal", "Window"]
        menu_bar = self.menuBar()

        for menu_name in major_menu_names:
            self.actions_.action_dicts[menu_name] = {}
            menu = menu_bar.addMenu(menu_name)
            self.actions_.menu_dict[menu_name] = menu

        window_menu = menu_bar.addMenu("Window")

        self.add_action("New", "File", QKeySequence.StandardKey.New)
        self.add_action("Open...", "File", QKeySequence.StandardKey.Open)
        self.add_separator("File")
        self.add_action("Close", "File", QKeySequence.StandardKey.Close)
        self.add_action("Save", "File", QKeySequence.StandardKey.Save)
        self.add_action("Save As...", "File", QKeySequence.StandardKey.SaveAs)
        self.add_separator("File")

        file_menu = self.actions_.menu_dict["File"]
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(sys.exit)
        file_menu.addAction(exit_action)

        self.add_action("Undo", "Edit", QKeySequence.StandardKey.Undo)
        self.add_action("Redo", "Edit", QKeySequence.StandardKey.Redo)
        self.add_separator("Edit")
        self.add_action("Cut", "Edit", QKeySequence.StandardKey.Cut)
        self.add_action("Copy", "Edit", QKeySequence.StandardKey.Copy)
        self.add_action("Paste", "Edit", QKeySequence.StandardKey.Paste)
        self.add_action("Clear", "Edit")
        self.add_action("Set Startup Size...", "Edit")

        self.add_action("Calc. Probabilities", "Matrix", checkable=True, disabled=True)
        self.add_action("Auto Probabilities", "Matrix", checkable=True, disabled=True, checked=True)
        self.add_separator("Matrix")
        self.add_action("Matrix Equation Form", "Matrix", checkable=True, disabled=True, checked=True)
        self.add_action("Compact Matrix Form", "Matrix", checkable=True, disabled=True)
        self.add_action("Scale/Rotation Form", "Matrix", checkable=True, disabled=True)
        self.add_separator("Matrix")
        self.add_action("Calc. X and Y Scale", "Matrix", disabled=True)

        design_action_names = [
            "New Transformation",
            "Duplicate Transformation",
            "Separator",
            "Rotate...",
            "Vertical Flip",
            "Horizontal Flip",
            "Separator",
            "Load Initial Polygon...",
            "Save Initial Polygon...",
            "Separator",
        ]

        for action_name in design_action_names:
            if action_name == "Separator":
                self.add_separator("Design")
            else:
                self.add_action(action_name, "Design", disabled=True)

        self.add_action("Show Fixed Points", "Design", checkable=True, disabled=True)
        self.add_action("Show Initial Polygon", "Design", checkable=True, disabled=True, checked=True)
        self.add_action("Clear Picture", "Design", checkable=True, disabled=True)
        self.add_separator("Design")
        self.add_action("Set Color...", "Design", disabled=True)

        self.add_action("Deterministic", "Fractal", checkable=True, disabled=True, checked=True)
        self.add_action("Random", "Fractal", checkable=True, disabled=True)
        self.add_separator("Fractal")
        self.add_action("Integer Math", "Fractal", checkable=True, disabled=True)
        self.add_action("Floating Point Math", "Fractal", checkable=True, disabled=True, checked=True)
        self.add_separator("Fractal")
        self.add_action("Do 1", "Fractal", disabled=True)
        self.add_action("Run...", "Fractal", disabled=True)

        self.add_action("Matrix", "Window")
        self.add_action("Fractal", "Window")
        self.add_action("Design", "Window")

        menu_bar.addMenu(window_menu)

    def add_action(
        self,
        action_name: str,
        menu_name: str,
        shortcut=None,
        checkable: bool = False,
        disabled: bool = False,
        checked: bool = False,
    ):
        action = QAction(action_name, self)
        action.setCheckable(checkable)
        menu = self.actions_.menu_dict[menu_name]
        if shortcut:
            action.setShortcut(shortcut)
        action.setDisabled(disabled)
        action.setChecked(checked)
        menu.addAction(action)
        self.actions_.action_dicts[menu.title()][action_name] = action

    def add_separator(self, menu_name: str):
        menu = self.actions_.menu_dict[menu_name]
        menu.addSeparator()

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                self.disable_all_actions("Matrix")
                self.disable_all_actions("Design")
                self.disable_all_actions("Fractal")
            elif self.fractal_window.isActiveWindow():
                self.disable_all_actions("Matrix")
                self.disable_all_actions("Design")
                self.enable_all_actions("Fractal")

    @staticmethod
    def toggle_window(window):
        if window.isVisible():
            window.hide()
        else:
            window.show()
            window.activateWindow()
            window.raise_()

    def disable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setDisabled(True)

    def enable_all_actions(self, menu_name: str):
        for action in self.actions_.action_dicts[menu_name].values():
            action.setEnabled(True)
