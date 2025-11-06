from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLineEdit, QMainWindow, QTableWidget, QVBoxLayout, QWidget


class MatrixWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        table = QTableWidget(2, 2, parent)

        layout = QVBoxLayout(parent)

        self.setLayout(layout)

        for i in range(2):
            for j in range(2):
                text_edit = QLineEdit(parent)
                text_edit.setMaxLength(3)
                table.setCellWidget(i, j, text_edit)

        layout.addWidget(table)


class MatrixWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._main = QWidget()
        self.setCentralWidget(self._main)
        layout = QVBoxLayout(self._main)

        matrix_widget = MatrixWidget()

        layout.addWidget(matrix_widget)

        self.setWindowTitle("Matrix")
