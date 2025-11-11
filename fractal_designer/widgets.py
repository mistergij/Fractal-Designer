from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QSizePolicy, QVBoxLayout


class SignLabel(QVBoxLayout):
    def __init__(self, sign: str = "+", parent=None):
        super().__init__(parent)

        sign_label = QLabel(sign)
        self.addWidget(sign_label)
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)


class MatrixInput(QGroupBox):
    def __init__(self, transformation_number: int = 0, parent=None):
        super().__init__(parent)

        self.setTitle(f"Transformation {transformation_number}")
        self.input_ = []

        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

        layout = QGridLayout(self)

        for i in range(2):
            for j in range(2):
                line_edit = QLineEdit()
                line_edit.setFixedWidth(100)
                layout.addWidget(line_edit, i, j, 1, 1)
                self.input_.append(line_edit)

        plus_sign = SignLabel("+")
        layout.addLayout(plus_sign, 0, 2, 2, 1)

        for i in range(2):
            line_edit = QLineEdit()
            line_edit.setFixedWidth(100)
            layout.addWidget(line_edit, i, 3, 1, 1)
            self.input_.append(line_edit)

        label = QLabel("p")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        line_edit = QLineEdit()
        line_edit.setFixedWidth(100)
        layout.addWidget(label, 0, 4, 1, 1)
        layout.addWidget(line_edit, 1, 4, 1, 1)


class CompactInput(QGroupBox):
    def __init__(self, transformation_number: int = 0, parent=None):
        super().__init__(parent)

        self.setTitle(f"Transformation {transformation_number}")
        self.input_ = []
        size_policy = QSizePolicy()
        size_policy.setHorizontalPolicy(QSizePolicy.Policy.Fixed)
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

        layout = QGridLayout(self)
        labels = ["a", "b", "c", "d", "e", "f", "p"]
        for i in range(7):
            label = QLabel(labels[i])
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            line_edit = QLineEdit()
            line_edit.setFixedWidth(100)
            layout.addWidget(label, 0, i, 1, 1)
            layout.addWidget(line_edit, 1, i, 1, 1)
            self.input_.append(line_edit)
