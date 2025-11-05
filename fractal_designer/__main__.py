import sys

from PySide6.QtWidgets import QApplication

from fractal_designer.windows.home import MainWindow

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    window.activateWindow()
    window.raise_()
    app.exec()
