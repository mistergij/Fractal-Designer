from PySide6.QtWidgets import QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fractal Designer")

        self.browser = QWebEngineView()

        initial_url = QUrl("http://127.0.0.1:8000")
        self.browser.setUrl(initial_url)

        self.setCentralWidget(self.browser)

        self.show()
