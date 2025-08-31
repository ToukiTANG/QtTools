import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout
from qfluentwidgets import GroupHeaderCardWidget, PushButton, FluentIcon, ComboBox, MessageBox, BodyLabel, IconWidget, PrimaryToolButton, InfoBar, \
    InfoBarPosition, InfoBarIcon

from app.common.config import SupportVideoFormat, VideoConversionSpeed
from app.components.ConversionMessageBox import ConversionMessageBox
from app.service.video_service import VideoFormatConverter


class VideoFormatConversionCard(GroupHeaderCardWidget):
    """
    视频格式转换card
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setTitle('格式转换')

        self.selectVideoPathButton = PushButton(text='选择文件')
        self.selectFormatComboBox = ComboBox()
        self.outputFolderButton = PushButton(text='选择输出文件夹')
        self.selectConversionQualityComboBox = ComboBox()
        self.conversionIcon = IconWidget(FluentIcon.INFO, self)
        self.conversionLabel = BodyLabel(text='点击右侧按钮开始转换')
        self.conversionButton = PrimaryToolButton(FluentIcon.PLAY, self)

        self.bottomHLayout = QHBoxLayout()

        self._initWidgets()
        self._initLayout()
        self._connectSignalToSlot()

    def _initWidgets(self):
        self.setBorderRadius(8)
        self.selectVideoPathButton.setFixedWidth(120)
        self.selectFormatComboBox.setFixedWidth(120)
        self.selectFormatComboBox.addItems(SupportVideoFormat.values())
        self.selectConversionQualityComboBox.setFixedWidth(120)
        self.selectConversionQualityComboBox.addItems(VideoConversionSpeed.labels())
        self.selectConversionQualityComboBox.setCurrentIndex(1)
        self.conversionIcon.setFixedSize(20, 20)

    def _initLayout(self):
        self.videoSelectedGroup = self.addGroup(
            icon=FluentIcon.FOLDER,
            title='选择需要转换的文件',
            content='',
            widget=self.selectVideoPathButton
        )

        self.formatSelectedGroup = self.addGroup(
            icon=FluentIcon.TILES,
            title='选择转换后的格式',
            content=self.selectFormatComboBox.currentText(),
            widget=self.selectFormatComboBox
        )

        self.outputFolderGroup = self.addGroup(
            icon=FluentIcon.FOLDER,
            title='输出文件目录',
            content='',
            widget=self.outputFolderButton
        )

        self.conversionSpeedGroup = self.addGroup(
            icon=FluentIcon.SPEED_HIGH,
            title='选择转换速度',
            content=VideoConversionSpeed.MEDIUM.description,
            widget=self.selectConversionQualityComboBox
        )
        self.conversionSpeedGroup.setSeparatorVisible(True)

        self.bottomHLayout.setContentsMargins(24, 15, 24, 20)
        self.bottomHLayout.setSpacing(10)
        self.bottomHLayout.addWidget(
            self.conversionIcon, 0, Qt.AlignmentFlag.AlignLeft
        )
        self.bottomHLayout.addWidget(
            self.conversionLabel, 0, Qt.AlignmentFlag.AlignLeft
        )
        self.bottomHLayout.addStretch(1)
        self.bottomHLayout.addWidget(
            self.conversionButton, 0, Qt.AlignmentFlag.AlignRight
        )

        self.vBoxLayout.addLayout(self.bottomHLayout)

    def _selectVideoFile(self):
        file, _ = QFileDialog.getOpenFileName(self, '选择文件', self.videoSelectedGroup.content())

        if file:
            if not SupportVideoFormat.is_supported(file):
                self._notSupportedMessage(title='该文件不是视频文件！', content=f'路径{file}的文件不是支持的视频文件！')
            else:
                self.videoSelectedGroup.setContent(file)
                self.outputFolderGroup.setContent(os.path.dirname(file))

    def _selectOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self, '选择文件夹', self.outputFolderGroup.content())
        if folder:
            self.outputFolderGroup.setContent(folder)

    def _selectFormat(self):
        self.formatSelectedGroup.setContent(self.selectFormatComboBox.currentText())

    def _selectConversionSpeed(self):
        # 获取当前选中的文本
        selectedLabel = self.selectConversionQualityComboBox.currentText()

        # 根据标签获取对应的枚举成员
        self.selectedSpeed = next((speed for speed in VideoConversionSpeed if speed.label == selectedLabel), None)
        self.conversionSpeedGroup.setContent(self.selectedSpeed.description)

    def _conversionVideo(self):

        if not self._checkParamValidity():
            return

        w = ConversionMessageBox(parent=self.window())
        w.show()

        inputFile = self.videoSelectedGroup.content()
        fileName = Path(inputFile).stem
        outputFile = Path(self.outputFolderGroup.content()) / (fileName + '.' + self.formatSelectedGroup.content())

        converter = VideoFormatConverter(inputFile, outputFile, preset=self.selectedSpeed.name.lower())
        converter.progressChanged.connect(w.setProgress)
        converter.finished.connect(w.conversionFinished)
        converter.start()

        if w.exec_():
            if w.conversionCompleted:
                # 完成转换打开文件夹
                os.startfile(self.outputFolderGroup.content())
            else:
                # 中断执行命令
                converter.terminate()
        else:
            w.close()

    def _connectSignalToSlot(self):
        self.selectVideoPathButton.clicked.connect(self._selectVideoFile)
        self.outputFolderButton.clicked.connect(self._selectOutputFolder)
        self.conversionButton.clicked.connect(self._conversionVideo)
        self.selectFormatComboBox.currentIndexChanged.connect(self._selectFormat)
        self.selectConversionQualityComboBox.currentIndexChanged.connect(self._selectConversionSpeed)

    def _notSupportedMessage(self, title: str, content: str):
        w = MessageBox(
            title=title,
            content=content,
            parent=self.window()
        )
        w.yesButton.setText("好的")
        w.cancelButton.hide()
        w.show()

    def _checkParamValidity(self) -> bool:
        if self.videoSelectedGroup.content() == '':
            info = ParamCheckWaringBar(content='未选择文件！', parent=self.window())
            info.show()
            return False
        if self.outputFolderGroup.content() == '':
            info = ParamCheckWaringBar(content='未选择输出文件夹！', parent=self.window())
            info.show()
            return False
        return True


class ParamCheckWaringBar(InfoBar):
    def __init__(self, content, title='参数错误', parent=None):
        super().__init__(icon=InfoBarIcon.WARNING, title=title, content=content, parent=parent)

    def warning(self, title, content, orient=Qt.Horizontal, isClosable=True, duration=5000,
                position=InfoBarPosition.TOP, parent=None):
        super().warning(title, content, orient, isClosable, duration, position, parent)
