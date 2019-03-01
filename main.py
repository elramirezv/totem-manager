from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox
from PyQt5.Qt import QTest, QTransform, QSound
from constants import *
import time
from selenium import webdriver
from driver_options import options, chromedriver_path

class Window(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background.setPixmap(QPixmap("images/background.png").scaled(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.main_layout = QGroupBox(self)
        self.main_layout.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setting_main_menu()
        self.show()
        self.setting_url_menu()

    def setting_main_menu(self):
        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col1, row3, 4*col, 4*col)
        self.url_main_button.setIcon(QIcon("images/web_url.png"))
        self.url_main_button.setIconSize(QSize(4*col, 4*col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

        self.videos_main_button = QPushButton("", self.main_layout)
        self.videos_main_button.setGeometry(col5, row3, 4*col, 4*col)
        self.videos_main_button.setIcon(QIcon("images/videos.png"))
        self.videos_main_button.setIconSize(QSize(4*col, 4*col))
        self.videos_main_button.setStyleSheet("background: transparent");
        self.videos_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

        self.images_main_button = QPushButton("", self.main_layout)
        self.images_main_button.setGeometry(col1, row6-100, 4*col, 4*col)
        self.images_main_button.setIcon(QIcon("images/fotos.png"))
        self.images_main_button.setIconSize(QSize(4*col, 4*col))
        self.images_main_button.setStyleSheet("background: transparent");
        self.images_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

        self.ads_main_button = QPushButton("", self.main_layout)
        self.ads_main_button.setGeometry(col5, row6-100, 4*col, 4*col)
        self.ads_main_button.setIcon(QIcon("images/ads.png"))
        self.ads_main_button.setIconSize(QSize(4*col, 4*col))
        self.ads_main_button.setStyleSheet("background: transparent");
        self.ads_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

    def hide_main_menu(self, menu):
        self.main_layout.hide()
        menu.show()

    def display_back_button(self, layout):
        self.back_label = QLabel("Regresar", layout)
        self.back_label.setGeometry(col4, row7, 3*col, row)
        self.back_label.setFont(QFont("Sans", 35))
        self.back_button = QPushButton("",layout)
        self.back_button.setGeometry(col1, row7, 3*col, 3*col)
        self.back_button.setIcon(QIcon("images/back.png"))
        self.back_button.setIconSize(QSize(col, col))
        self.back_button.setStyleSheet("background: transparent");
        self.back_button.clicked.connect(lambda: self.go_back(layout))
        self.back_label.show()
        self.back_button.show()

    def go_back(self, layout):
        layout.hide()
        self.main_layout.show()

    def setting_url_menu(self):
        self.url_layout = QGroupBox(self)
        self.url_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Inserte URL de su página web", self.url_layout)
        self.web_label.setGeometry(0, row3, col10, row)
        self.web_label.setStyleSheet("text-align: center")
        self.web_label.setFont(QFont("Sans", 35))
        self.web_name = QLineEdit("", self.url_layout)
        self.web_name.setGeometry(col2, row4, col*4, row/2)
        self.web_name.setFont(QFont("Sans", 20))
        self.web_name.setPlaceholderText("Ejemplo: www.gooogle.com")
        self.accept_button = QPushButton("Aceptar", self.url_layout)
        self.accept_button.setGeometry(col6, row4, col*2, row/2)
        self.accept_button.clicked.connect(lambda: self.openBrowser(self.web_name.text()))
        self.display_back_button(self.url_layout)

    def small_screen(self, layout):
        self.count = []
        self.setGeometry(col9, row9, col, row)
        self.setWindowOpacity(0)
        layout.hide()
        self.small_button = QPushButton("", self)
        self.small_button.setGeometry(0, 0, col, row)
        self.small_button.clicked.connect(self.addNumber)
        self.small_button.show()

    def addNumber(self):
        self.count.append(1)
        if len(self.count) >= 3:
            self.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.setWindowOpacity(1)
            self.small_button.hide()
            self.url_layout.show()
            self.chrome_driver.close()

    def openBrowser(self, name):
        self.web_name.setText("")
        self.chrome_driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
        self.chrome_driver.get("https://"+name)
        self.small_screen(self.url_layout)


if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
