from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog
from PyQt5.Qt import QTest, QTransform, QSound
from clases import SmallScreen, VideoScreen, WebBrowser
from constants import *
import time
from selenium import webdriver
from driver_options import options, chromedriver_path
import subprocess
import os
import shutil
import stat

class Window(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background.setPixmap(QPixmap("images/background.png").scaled(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.main_layout = QGroupBox(self)
        self.main_layout.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setting_main_menu()
        self.show()
        self.setting_url_menu()
        self.setting_videos_menu()
        self.setting_photos_menu()

    def setting_main_menu(self):
        # Setea todos los botones del menú principal (solamente los crea)
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
        self.videos_main_button.clicked.connect(lambda: self.hide_main_menu(self.video_layout))

        self.images_main_button = QPushButton("", self.main_layout)
        self.images_main_button.setGeometry(col1, row6-100, 4*col, 4*col)
        self.images_main_button.setIcon(QIcon("images/fotos.png"))
        self.images_main_button.setIconSize(QSize(4*col, 4*col))
        self.images_main_button.setStyleSheet("background: transparent");
        self.images_main_button.clicked.connect(lambda: self.hide_main_menu(self.photo_layout))

        self.ads_main_button = QPushButton("", self.main_layout)
        self.ads_main_button.setGeometry(col5, row6-100, 4*col, 4*col)
        self.ads_main_button.setIcon(QIcon("images/ads.png"))
        self.ads_main_button.setIconSize(QSize(4*col, 4*col))
        self.ads_main_button.setStyleSheet("background: transparent");
        self.ads_main_button.clicked.connect(lambda: self.hide_main_menu(self.url_layout))

    def setting_url_menu(self):
        # Setea el layout del web_url menu
        self.url_layout = QGroupBox(self)
        self.url_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Escribe el URL de tu página web", self.url_layout)
        self.web_label.setGeometry(col1, row3, col10, row)
        self.web_label.setStyleSheet("text-align: center")
        self.web_label.setFont(QFont("Sans", 35))
        self.web_name = QLineEdit("", self.url_layout)
        self.web_name.setGeometry(col2, row4, col*4, row/2)
        self.web_name.setFont(QFont("Sans", 20))
        self.web_name.setPlaceholderText("Ej: www.google.com")
        self.accept_button = QPushButton("Aceptar", self.url_layout)
        self.accept_button.setGeometry(col6, row4, col*2, row/2)
        self.accept_button.clicked.connect(lambda: self.openBrowser(self.web_name.text()))
        self.display_back_button(self.url_layout)

    def setting_photos_menu(self):
        # Setea el layout del menu de fotos
        self.photo_layout = QGroupBox(self)
        self.photo_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Selecciona la carpeta de fotos", self.photo_layout)
        self.web_label.setGeometry(col1, row3, col10, row)
        self.web_label.setStyleSheet("text-align: center")
        self.web_label.setFont(QFont("Sans", 35))
        self.load_button = QPushButton("Cargar", self.photo_layout)
        self.load_button.setGeometry(col6, row4, col*2, row/2)
        self.load_button.clicked.connect(self.load_photos)
        self.photo_play_button = QPushButton("Reproducir", self.photo_layout)
        self.photo_play_button.setGeometry(col6, row6, col*2, row/2)
        self.photo_play_button.clicked.connect(self.display_slideshow)
        self.photo_play_button.hide()
        self.display_back_button(self.photo_layout)

    def setting_videos_menu(self):
        # Setea el layout del menu de videos
        self.video_layout = QGroupBox(self)
        self.video_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Selecciona la carpeta de video/s", self.video_layout)
        self.web_label.setGeometry(col1, row3, col10, row)
        self.web_label.setStyleSheet("text-align: center")
        self.web_label.setFont(QFont("Sans", 35))
        self.load_button = QPushButton("Cargar", self.video_layout)
        self.load_button.setGeometry(col6, row4, col*2, row/2)
        self.load_button.clicked.connect(self.load_video)
        self.video_play_button = QPushButton("Reproducir", self.video_layout)
        self.video_play_button.setGeometry(col6, row6, col*2, row/2)
        self.video_play_button.clicked.connect(self.display_video_player)
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
        self.back_label = QLabel("Regresar", layout)
        self.back_label.setGeometry(col2+60, row7+10, 3*col, row)
        self.back_label.setFont(QFont("Sans", 20))
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


    def display_video_player(self):
        self.video_player = VideoScreen(self.ddir)
        self.video_player.show()
        self.small_icon = SmallScreen(driver=self.video_player)
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
        # Este método setea el driver de chrome y luego corre el 'script.sh' para abrir
        # una nueva terminal, luego ejecuta 'app.py' en el puerto 5000 donde se encuentra el carrusel
        self.chrome_driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
        # Esta funcion es la que abre la segunda terminal, aquí se le debería entregar a la app
        # la ubicación de donde se encuentren las fotos (self.ddir)
        cwd = os.getcwd()
        subprocess.Popen('python app.py {}'.format(cwd + '/static'), stdout=subprocess.PIPE)
        # QWait para que se alcance a cargar el servidor de app.py
        QTest.qWait(2000)
        self.chrome_driver.get("http://localhost:5000/")
        self.small_icon = SmallScreen(driver = self.chrome_driver)
        self.small_icon.show()
        self.small_icon.activateWindow()

    def openBrowser(self, name):
        self.web_name.setText("")
        
        if name != "":
            self.browser_window = QMainWindow()
            self.browser_window.setGeometry(0,0,col10,row10)
            self.web_browser = WebBrowser("https://"+name)
            self.browser_window.setCentralWidget(self.web_browser)
            self.browser_window.show()
            self.small_icon = SmallScreen(self.web_browser)
            self.small_icon.show()
            self.small_icon.activateWindow()


if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
