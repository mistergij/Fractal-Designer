from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow


class MenuWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.actions: dict[str, QAction] = {}

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        # exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        self.actions["Exit"] = exit_action

        menu_bar.addMenu(file_menu)

        view_menu = menu_bar.addMenu("View")

        open_fractal_window = QAction("Fractal", self)
        view_menu.addAction(open_fractal_window)
        self.actions["Fractal"] = open_fractal_window

        menu_bar.addMenu(view_menu)
