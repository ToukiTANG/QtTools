import sys

from PyQt5.QtCore import Qt, QSize, QEventLoop, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, FluentIcon, NavigationItemPosition, SplashScreen

import app.resource.resources_rc
from app.views.home_interface import HomeInterface
from app.views.video_format_interface import VideoFormatInterface


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        self.initWindow()

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.show()

        self.splashScreenShowTime()

        self.homeInterface = HomeInterface(self)
        self.videoFormatInterface = VideoFormatInterface()

        self.initNavigation()
        self._onFinished()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '主页', isTransparent=True)
        formatParentItem = self.navigationInterface.addItem(
            routeKey="formatParent",
            icon=FluentIcon.SYNC,  # 图标
            text="格式转换",
            selectable=False,
            position=NavigationItemPosition.TOP
        )
        formatParentItem.setObjectName('formatParent')
        self.addSubInterface(self.videoFormatInterface, FluentIcon.VIDEO, text='视频', parent=formatParentItem, isTransparent=True)
        # 设置展开宽度
        self.navigationInterface.setExpandWidth(150)
        # 这行代码必须在 setExpandWidth() 后面调用，设置默认展开
        self.navigationInterface.setCollapsible(False)

    def initWindow(self):
        self.resize(1000, 700)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/icons/China_Railways.svg'))
        self.setWindowTitle('QtTools')

        desktop = QApplication.desktop().availableGeometry()
        desktopW, desktopH = desktop.width(), desktop.height()
        self.move(desktopW // 2 - self.width() // 2, desktopH // 2 - self.height() // 2)

    def _onFinished(self):
        self.splashScreen.finish()

    def splashScreenShowTime(self):
        loop = QEventLoop(self)
        QTimer.singleShot(2000, loop.quit)
        loop.exec()

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()
