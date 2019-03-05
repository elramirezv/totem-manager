from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from constants import *

class SmallScreen(QWidget):
    def __init__(self, driver=None, parent = None):
        super().__init__(parent)
        self.setWindowOpacity(0.05)
        self.setGeometry(0, 0, col, row)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.chrome_driver = driver
        self.count = []
        self.small_button = QPushButton("", self)
        self.small_button.setGeometry(0, 0, col, row)
        self.small_button.clicked.connect(self.addNumber)
        self.small_button.show()

    def addNumber(self):
        if len(self.count) == 0:
            self.begin = time.time()
        self.count.append(1)
        if len(self.count) >= 5:
            if time.time() - self.begin > 10:
                self.count = []
                self.begin = time.time()
            else:
                self.close()
                if self.chrome_driver:
                    self.chrome_driver.close()
