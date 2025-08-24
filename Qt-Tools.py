import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from app.views.main_window import MainWindow

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
