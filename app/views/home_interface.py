from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea

from components.info_layout import InfoLayout


class HomeInterface(ScrollArea):
    """
    首页interface，可以放一些描述性信息，如公告、使用帮助等
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)
        self.infoLayout = InfoLayout(self.view)

        self._initWidget()

    def _initWidget(self):
        self.setWidget(self.view)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.resize(780, 800)
        self.setObjectName("packageInterface")
        self.enableTransparentBackground()
