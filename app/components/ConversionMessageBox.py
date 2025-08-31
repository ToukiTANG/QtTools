from PyQt5.QtCore import pyqtSignal
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ProgressBar


class ConversionMessageBox(MessageBoxBase):
    closeSignal = pyqtSignal()

    def __init__(self, yesText='中断任务', cancelText='知道了', title='请等待转换', parent=None):
        super().__init__(parent=parent)
        self.conversionCompleted = False
        self.titleLabel = SubtitleLabel(title, self)
        self.yesButton.setText(yesText)
        self.cancelButton.setText(cancelText)
        self.conversionProgress = ProgressBar()

        self._initWidget()
        self._initLayout()

    def _initWidget(self):
        self.widget.setMinimumWidth(350)
        self.conversionProgress.setRange(0, 100)
        # 初始状态禁止
        self.cancelButton.setDisabled(True)

    def _initLayout(self):
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.conversionProgress)

    def setProgress(self, value):
        self.conversionProgress.setValue(value)

    def conversionFinished(self):
        self.yesButton.setText('打开文件夹')
        self.cancelButton.setDisabled(False)
        self.conversionCompleted = True
