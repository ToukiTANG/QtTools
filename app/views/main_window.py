import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QApplication
from qfluentwidgets import SubtitleLabel, setFont, FluentWindow, FluentIcon, NavigationItemPosition

import app.resource.resources_rc
from app.views.home_interface import HomeInterface
from app.views.video_format_interface import VideoFormatInterface


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignHCenter)  # type: ignore
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignHCenter)
        self.setObjectName(text.replace(' ', '-'))
        # leave some space for title bar
        self.hBoxLayout.setContentsMargins(0, 32, 0, 0)


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.homeInterface = HomeInterface(self)
        self.formatInterface = Widget('Format conversion Interface', self)
        self.videoFormatInterface = VideoFormatInterface()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '主页')
        self.addSubInterface(self.formatInterface, FluentIcon.SYNC, '格式转换', NavigationItemPosition.SCROLL)
        self.addSubInterface(self.videoFormatInterface, FluentIcon.MOVIE, text='视频', parent=self.formatInterface)
        # 设置展开宽度
        self.navigationInterface.setExpandWidth(150)
        # 这行代码必须在 setExpandWidth() 后面调用，设置默认展开
        self.navigationInterface.setCollapsible(False)

        item = self.navigationInterface.widget(self.formatInterface.objectName())
        item.clicked.disconnect()  # 取消默认点击逻辑
        item.clicked.connect(lambda: None)  # 改成空操作

    def initWindow(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon(':/icons/China_Railways.svg'))
        self.setWindowTitle('QtTools')

        desktop = QApplication.desktop().availableGeometry()
        desktopW, desktopH = desktop.width(), desktop.height()
        self.move(desktopW // 2 - self.width() // 2, desktopH // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
