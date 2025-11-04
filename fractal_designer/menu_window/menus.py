from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow

from fractal_designer.windows.fractal import FractalWindow


class MenuWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        menu_bar.addMenu(file_menu)

        view_menu = menu_bar.addMenu("View")

        open_fractal_window = QAction("Fractal", self)
        open_fractal_window.triggered.connect(lambda checked: self.toggle_fractal(self.fractal))
        view_menu.addAction(open_fractal_window)

        menu_bar.addMenu(view_menu)

        self.fractal = FractalWindow()

    def toggle_fractal(self, window):
        window.hide() if self.fractal.isVisible() else window.show()
