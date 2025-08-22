import sys

from PyQt5.QtWidgets import QApplication

from app.views.main_window import MainWindow

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec_()
