from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog
from PyQt5.Qt import QTest, QTransform, QSound
from clases import SmallScreen, VideoScreen, WebBrowser, PasswordWindow, MainWindow, PhotoViewer
from constants import *
import time
import subprocess
import os
import shutil
import stat
import sys
from PIL import Image

class Window(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.time_interval = 0.05
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
        self.processing_photos =False
    def create_password(self, function):
        self.password_editor = PasswordWindow(function)
        self.password_editor.show()


    def setting_main_menu(self):
        # Setea todos los botones del menú principal (solamente los crea)
        self.close_button = QPushButton(self.main_layout)
        self.close_button.setGeometry(col9, row/4, col/3, col/3)
        self.close_button.setIcon(QIcon("images/close.png"))
        self.close_button.setIconSize(QSize(col/3, col/3))
        self.close_button.setStyleSheet("background: transparent")
        self.close_button.clicked.connect(exit)

        self.url_main_button = QPushButton(self.main_layout)
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
        self.html_button = QPushButton('Usar Html local', self.url_layout)
        self.html_button.setGeometry(col4, row5 + row/2, col2, row/2)
        self.html_button.setFont(QFont("Sans", 20))
        self.html_button.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.html_button.clicked.connect(self.loadhtml)

        self.display_back_button(self.url_layout)

    def setting_photos_menu(self):
        # Setea el layout del menu de fotos
        self.photo_layout = QGroupBox(self)
        self.photo_layout.setFixedSize(col10, row10)
        self.web_label = QLabel("Seleccione la carpeta de fotos", self.photo_layout)
        self.web_label.setGeometry(0, row2, col10, row)
        self.web_label.setAlignment(Qt.AlignCenter)
        self.web_label.setFont(QFont("Sans", 35))
        self.time_edit = QLabel(str(self.time_interval) + "s", self.photo_layout)
        self.time_edit.setFont(QFont("Sans" , 20))
        self.time_edit.setGeometry(col4, row5 + row/2, col2, row/2)
        self.time_edit.setAlignment(Qt.AlignCenter)
        self.time_edit.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.add_time = QPushButton('+ 0.1s', self.photo_layout)
        self.add_time.setFont(QFont("Sans", 15))
        self.add_time.setGeometry(col6 + col2/8, row5 + row/2, col, row/2)
        self.add_time.clicked.connect(lambda: self.change_interval(0.1))
        self.add_time.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.add_time2 = QPushButton('+ 1.0s', self.photo_layout)
        self.add_time2.setFont(QFont("Sans", 15))
        self.add_time2.setGeometry(col7 + col4/8, row5 + row/2, col, row/2)
        self.add_time2.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.add_time2.clicked.connect(lambda: self.change_interval(1))
        self.sub_time = QPushButton('- 0.1s', self.photo_layout)
        self.sub_time.setFont(QFont("Sans", 15))
        self.sub_time.setGeometry(col2 + col6/8, row5 + row/2, col, row/2)
        self.sub_time.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.sub_time.clicked.connect(lambda: self.change_interval(-0.1))
        self.sub_time.setEnabled(False)
        self.sub_time2 = QPushButton('- 1.0s', self.photo_layout)
        self.sub_time2.setFont(QFont("Sans", 15))
        self.sub_time2.setGeometry(col + col4/8, row5 + row/2, col, row/2)
        self.sub_time2.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")
        self.sub_time2.clicked.connect(lambda: self.change_interval(-1))
        self.sub_time2.setEnabled(False)
        self.load_button = QPushButton("CARGAR", self.photo_layout)
        self.load_button.setFont(QFont("Sans", 35))
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

    def change_interval(self, value):
        if self.time_interval == 0.05:
            self.time_interval = value
        else:
            self.time_interval += value
        self.time_interval = round(self.time_interval, 2)
        self.sub_time.setEnabled(True)
        self.sub_time2.setEnabled(True)
        if self.time_interval < 1:
            self.sub_time2.setEnabled(False)
            if self.time_interval == 0:
                self.sub_time.setEnabled(False)
                self.time_interval = 0.05
        self.time_edit.setText(str(self.time_interval) + 's')

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
        if not self.processing_photos:
            self.video_player = VideoScreen(self.ddir)
            self.video_player.show()
            self.small_icon = SmallScreen(driver=self.video_player, password = self.password_editor)
            self.small_icon.show()
            self.small_icon.activateWindow()
            self.video_player.player.play()

    def load_photos(self):
        self.ddir = QFileDialog.getExistingDirectory(self)
        self.video_play_button.hide()
        self.photo_play_button.show()

    def loadhtml(self):
        self.ddir = QFileDialog.getOpenFileName(self)[0]
        print(self.ddir)
        self.video_play_button.hide()
        self.create_password(self.open_html)

    def load_video(self):
        self.ddir = QFileDialog.getExistingDirectory(self)
        self.video_play_button.show()
        self.photo_play_button.hide()

    def display_slideshow(self):
        if not self.processing_photos:
            cwd = os.getcwd()
            dir = os.listdir(self.ddir)
            photos = [x for x in dir if x.endswith('.jpg') or x.endswith('.png') or x.endswith('.jpeg')]
            self.slideshow_window = PhotoViewer(self, photos, self.time_interval, self.ddir)
            self.slideshow_window.show()
            self.small_icon = SmallScreen(driver=self.slideshow_window, password = self.password_editor, photos= True)
            self.small_icon.show()
            self.small_icon.activateWindow()

    def change_slideshow(self, image):
        image = self.ddir + '/' + image
        im = Image.open(image)
        w,h = im.size
        while w > SCREEN_WIDTH or h > SCREEN_HEIGHT:
            w *= 0.95
            h *= 0.95
        self.slideshow_window.label.setPixmap(QPixmap(image).scaled(w,h))

    def open_html(self):
        if not self.processing_photos:
            fileName = self.ddir
            if fileName:
                self.browser_window = MainWindow(WebBrowser(fileName, local = True))
                self.browser_window.show()
                self.small_icon = SmallScreen(self.browser_window, password = self.password_editor)
                self.small_icon.show()
                self.small_icon.activateWindow()


    def openBrowser(self):
        if not self.processing_photos:
            name = self.web_name.text()
            self.web_name.setText("")
            if name != "":
                self.browser_window = MainWindow(WebBrowser("https://"+name))
                self.browser_window.show()
                self.small_icon = SmallScreen(self.browser_window, password = self.password_editor)
                self.small_icon.show()
                self.small_icon.activateWindow()



if __name__ == "__main__":
    app = QApplication([])
    editor = Window()
    app.exec_()
