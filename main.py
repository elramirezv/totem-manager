from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog
from PyQt5.Qt import QTest, QTransform, QSound
from clases import SmallScreen, VideoScreen, WebBrowser, PasswordWindow
from constants import *
import time
import subprocess
import os
import shutil
import stat

class Window(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background.setPixmap(QPixmap("images/background.jpg").scaled(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.main_layout = QGroupBox(self)
        self.main_layout.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setting_main_menu()
        self.show()
        self.setting_url_menu()
        self.setting_videos_menu()
        self.setting_photos_menu()
        subprocess.Popen('mkdir static',stdout=subprocess.PIPE, shell=True)

    def create_password(self, function):
        self.password_editor = PasswordWindow(function)
        self.password_editor.show()


    def setting_main_menu(self):
        # Setea todos los botones del menú principal (solamente los crea)
        self.url_main_button = QPushButton("", self.main_layout)
        self.url_main_button.setGeometry(col4 + col/2, row4 + row/2, col, col)
        self.url_main_button.setIcon(QIcon("images/url.svg"))
        self.url_main_button.setIconSize(QSize(col, col))
        self.url_main_button.setStyleSheet("background: transparent");
        self.url_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

        self.videos_main_button = QPushButton("", self.main_layout)
        self.videos_main_button.setGeometry(col7 + col/2, row4+ row/2, col, col)
        self.videos_main_button.setIcon(QIcon("images/videos.svg"))
        self.videos_main_button.setIconSize(QSize(col, col))
        self.videos_main_button.setStyleSheet("background: transparent");
        self.videos_main_button.clicked.connect(lambda: self.hide_main_menu(self.video_layout))

        self.images_main_button = QPushButton("", self.main_layout)
        self.images_main_button.setGeometry(col1 + col/2, row4 + row/2, col, col)
        self.images_main_button.setIcon(QIcon("images/fotos.svg"))
        self.images_main_button.setIconSize(QSize(col, col))
        self.images_main_button.setStyleSheet("background: transparent");
        self.images_main_button.clicked.connect(lambda: self.hide_main_menu(self.photo_layout))

    def setting_url_menu(self):
        # Setea el layout del web_url menu
        self.url_layout = QGroupBox(self)
        self.url_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Escriba el URL de tu página web", self.url_layout)
        self.web_label.setGeometry(0, row2, col10, row)
        self.web_label.setAlignment(Qt.AlignCenter)
        self.web_label.setStyleSheet("text-align: center")
        self.web_label.setFont(QFont("Sans", 35))
        self.web_name = QLineEdit("", self.url_layout)
        self.web_name.setGeometry(col, row3 + row/2, col8, row/2)
        self.web_name.setFont(QFont("Sans", 20))
        self.web_name.setPlaceholderText("Ej: www.fastersoluciones.cl")
        self.accept_button = QPushButton("ACEPTAR", self.url_layout)
        self.accept_button.setGeometry(col4, row4 + row/2, col2, row/2)
        self.accept_button.setFont(QFont("Sans", 20))
        self.accept_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.accept_button.clicked.connect(lambda: self.create_password(self.openBrowser))
        self.display_back_button(self.url_layout)

    def setting_photos_menu(self):
        # Setea el layout del menu de fotos
        self.photo_layout = QGroupBox(self)
        self.photo_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Seleccione la carpeta de fotos", self.photo_layout)
        self.web_label.setGeometry(0, row2, col10, row)
        self.web_label.setAlignment(Qt.AlignCenter)
        self.web_label.setFont(QFont("Sans", 35))
        self.load_button = QPushButton("CARGAR", self.photo_layout)
        self.load_button.setFont(QFont("Sans", 25))
        self.load_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.load_button.setGeometry(col, row3 + row/2, col8, row/2)
        self.load_button.clicked.connect(self.load_photos)
        self.photo_play_button = QPushButton("REPRODUCIR", self.photo_layout)
        self.photo_play_button.setGeometry(col, row4 + row/2, col8, row/2)
        self.photo_play_button.setFont(QFont("Sans", 25))
        self.photo_play_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.photo_play_button.clicked.connect(lambda: self.create_password(self.display_slideshow))
        self.photo_play_button.hide()
        self.display_back_button(self.photo_layout)

    def setting_videos_menu(self):
        # Setea el layout del menu de videos
        self.video_layout = QGroupBox(self)
        self.video_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Seleccione la carpeta de videos", self.video_layout)
        self.web_label.setGeometry(0, row2, col10, row)
        self.web_label.setAlignment(Qt.AlignCenter)
        self.web_label.setFont(QFont("Sans", 35))
        self.load_button = QPushButton("CARGAR", self.video_layout)
        self.load_button.setFont(QFont("Sans", 25))
        self.load_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.load_button.setGeometry(col, row3 + row/2, col8, row/2)
        self.load_button.clicked.connect(self.load_video)
        self.video_play_button = QPushButton("Reproducir", self.video_layout)
        self.video_play_button.setGeometry(col, row4 + row/2, col8, row/2)
        self.video_play_button.setFont(QFont("Sans", 25))
        self.video_play_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.video_play_button.clicked.connect(lambda: self.create_password(self.display_video_player))
        self.video_play_button.hide()
        self.display_back_button(self.video_layout)

    def hide_main_menu(self, menu):
        # Se llama cada vez que se aprieta algún botón del menu principal.
        # Esconde el main y abre el que fue presionado.
        self.web_name.setText("")
        self.main_layout.hide()
        menu.show()

    def display_back_button(self, layout):
        # Este método despliega el botón de volver al menú principal en cualquier pagina
        # Es llamado en todas las páginas del programa.
        self.back_button = QPushButton("",layout)
        self.back_button.setGeometry(col, row9, col,col)
        self.back_button.setIcon(QIcon("images/back.png"))
        self.back_button.setIconSize(QSize(col, col))
        self.back_button.setStyleSheet("background: transparent; border-radius: 30px")
        self.back_button.clicked.connect(lambda: self.go_back(layout))
        self.back_button.show()

    def go_back(self, layout):
        layout.hide()
        self.main_layout.show()


    def display_video_player(self):
        self.video_player = VideoScreen(self.ddir)
        self.video_player.show()
        self.small_icon = SmallScreen(driver=self.video_player, password = self.password_editor)
        self.small_icon.show()
        self.small_icon.activateWindow()
        self.video_player.player.play()

    def load_photos(self):
        self.ddir = QFileDialog.getExistingDirectory(self)
        cwd = os.getcwd()
        subprocess.Popen('del /q "{}/static"'.format(cwd), stdout=subprocess.PIPE, shell=True)
        subprocess.Popen('xcopy "{}" "{}/static" /E'.format(self.ddir, cwd), stdout=subprocess.PIPE)
        self.video_play_button.hide()
        self.photo_play_button.show()

    def load_video(self):
        self.ddir = QFileDialog.getExistingDirectory(self)
        self.video_play_button.show()
        self.photo_play_button.hide()

    def display_slideshow(self):
        cwd = os.getcwd()
        subprocess.Popen('python app.py {}'.format(cwd + '/static'), stdout=subprocess.PIPE)
        # QWait para que se alcance a cargar el servidor de app.py
        QTest.qWait(3000)
        self.slideshow_window = QMainWindow()
        self.slideshow_window.setWindowFlags(Qt.FramelessWindowHint)
        self.slideshow_window.setGeometry(0,0,col10,row10)
        self.slideshow_browser = WebBrowser("http://localhost:5000/")
        self.slideshow_window.setCentralWidget(self.slideshow_browser)
        self.slideshow_window.show()
        self.small_icon = SmallScreen(driver=self.slideshow_window, password = self.password_editor)
        self.small_icon.show()
        self.small_icon.activateWindow()

    def openBrowser(self):
        name = self.web_name.text()
        self.web_name.setText("")
        if name != "":
            self.browser_window = QMainWindow()
            self.browser_window.setWindowFlags(Qt.FramelessWindowHint)
            self.browser_window.setGeometry(0,0,col10,row10)
            self.web_browser = WebBrowser("https://"+name)
            self.browser_window.setCentralWidget(self.web_browser)
            self.browser_window.show()
            self.small_icon = SmallScreen(self.browser_window, password = self.password_editor)
            self.small_icon.show()
            self.small_icon.activateWindow()


if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
