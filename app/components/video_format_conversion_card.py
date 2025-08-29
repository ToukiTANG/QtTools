from PyQt5.QtWidgets import QFileDialog
from qfluentwidgets import GroupHeaderCardWidget, PushButton, FluentIcon, ComboBox


class VideoFormatConversionCard(GroupHeaderCardWidget):
    """
    视频格式转换card
    """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setTitle('格式转换')

        self.selectVideoPathButton = PushButton(text='选择文件')
        self.selectFormatComboBox = ComboBox()

        self._initWidgets()
        self._initLayout()
        self._connectSignalToSlot()

    def _initWidgets(self):
        self.setBorderRadius(8)
        self.selectVideoPathButton.setFixedWidth(120)
        self.selectFormatComboBox.setFixedWidth(120)

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
            content='',
            widget=self.selectFormatComboBox
        )

    def _selectVideoFile(self):
        file, _ = QFileDialog.getOpenFileName(self, '选择文件', self.videoSelectedGroup.content())

        if file:
            self.videoSelectedGroup.setContent(file)

    def _connectSignalToSlot(self):
        self.selectVideoPathButton.clicked.connect(self._selectVideoFile)
