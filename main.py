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
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background.setPixmap(QPixmap("images/background.png").scaled(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.main_layout = QGroupBox(self)
        self.main_layout.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.display_main_menu()
        self.show()

    def display_main_menu(self):
        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col1, row3, 4*col, 4*col)
        self.url_main_button.setIcon(QIcon("images/item1.png"))
        self.url_main_button.setIconSize(QSize(4*col, 4*col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.display_url_menu))

        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col5, row3, 4*col, 4*col)
        self.url_main_button.setIcon(QIcon("images/item1.png"))
        self.url_main_button.setIconSize(QSize(4*col, 4*col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.display_url_menu))

        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col1, row6-100, 4*col, 4*col)
        self.url_main_button.setIcon(QIcon("images/item1.png"))
        self.url_main_button.setIconSize(QSize(4*col, 4*col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.display_url_menu))

        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col5, row6-100, 4*col, 4*col)
        self.url_main_button.setIcon(QIcon("images/item1.png"))
        self.url_main_button.setIconSize(QSize(4*col, 4*col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.display_url_menu))

    def hide_main_menu(self, menu):
        self.main_layout.hide()
        menu()


    def display_url_menu(self):
        self.url_layout = QGroupBox(self)
        self.url_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Inserte URL de su página web: ", self.url_layout)
        self.web_label.setGeometry(col2, row3, col, row/2)
        self.web_name = QLineEdit("", self.url_layout)
        self.web_name.setGeometry(col4, row3, col*2, row/2)
        self.accept_button = QPushButton("Aceptar", self.url_layout)
        self.accept_button.setGeometry(col6, row3, col*2, row/2)
        self.accept_button.clicked.connect(lambda: self.openBrowser(self.web_name.text()))
        self.url_layout.show()


    def openBrowser(self, name):
        print(self.web_name.text())
        self.chrome_driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
        self.chrome_driver.get("https://"+name)


if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
