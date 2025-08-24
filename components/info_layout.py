from qfluentwidgets import FlowLayout, DisplayLabel


class InfoLayout(FlowLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.info = DisplayLabel()

        self._initWidget()

    def _initWidget(self):
        self.info.setText("Info")
        self.addWidget(self.info)
