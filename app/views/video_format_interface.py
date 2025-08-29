from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import ScrollArea

from app.components.box_layout import BoxLayout
from app.components.video_format_conversion_card import VideoFormatConversionCard


class VideoFormatInterface(ScrollArea):
    """
    视频转换interface
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.view = QWidget()
        self.vBoxLayout = BoxLayout(self.view)
        self.formatConversionCard = VideoFormatConversionCard()

        self._initWidget()

    def _initWidget(self):
        self.setWidget(self.view)
        self.setAcceptDrops(True)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.vBoxLayout.addWidget(self.formatConversionCard, 0, Qt.AlignmentFlag.AlignTop)

        self.setObjectName("videoFormatInterface")
        self.enableTransparentBackground()
