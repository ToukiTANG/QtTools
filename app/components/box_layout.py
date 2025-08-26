from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt


class BoxLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._initWidget()

    def _initWidget(self):

        self.setSpacing(10)
        self.setContentsMargins(0, 0, 10, 10)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)

