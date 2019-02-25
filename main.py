from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
import time
from selenium import webdriver
from driver_options import options, chromedriver_path


class Window(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.web_label = QLabel("Inserte URL de su página web: ", self)
        self.web_label.setGeometry(10, 10, SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.05)
        self.web_name = QLineEdit("", self)
        self.web_name.setGeometry(SCREEN_WIDTH*0.2+10, 10, SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.05)
        self.accept_button = QPushButton("Aceptar", self)
        self.accept_button.setGeometry(SCREEN_WIDTH*0.4+10, 10, SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.05)
        self.accept_button.clicked.connect(lambda: self.openBrowser(self.web_name.text()))

        self.show()

    def openBrowser(self, name):
        print(self.web_name.text())
        self.chrome_driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
        self.chrome_driver.get("https://"+name)


if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
