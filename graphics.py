import sys

from PySide6.QtGui import QAction, QKeySequence, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QMenuBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set title
        self.setWindowTitle("Transformations")

        # Create Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        menu.addMenu(file_menu)

        # Define and add exit action on non-MacOS systems
        if sys.platform != "darwin":
            exit_action = QAction("Exit", self)
            exit_action.setShortcut(QKeySequence.Quit)
            exit_action.triggered.connect(self.close)
            
            file_menu.addAction(exit_action)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()
