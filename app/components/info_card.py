from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import SimpleCardWidget, DisplayLabel


class InfoCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.test = DisplayLabel()
        self.qv = QVBoxLayout(self)

        self._initWidget()

    def _initWidget(self):
        self.test.setText("Home")
        self.qv.addWidget(self.test)

