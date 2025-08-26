from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import ScrollArea

from app.components.box_layout import BoxLayout
from app.components.info_card import InfoCard


class HomeInterface(ScrollArea):
    """
    首页interface，可以放一些描述性信息，如公告、使用帮助等
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)
        self.vBoxLayout = BoxLayout(self.view)

        self.infoCard = InfoCard()

        self._initWidget()

    def _initWidget(self):
        self.setWidget(self.view)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vBoxLayout.addWidget(self.infoCard, 0, Qt.AlignmentFlag.AlignTop)

        self.setObjectName("homeInterface")
        self.enableTransparentBackground()
