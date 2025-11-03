from PySide6.QtGui import QAction, QKeySequence, QPainter
from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title
        self.setWindowTitle("Transformations")

        # Create Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        menu.addMenu(file_menu)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)
