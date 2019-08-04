from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication, QUrl
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog
from PyQt5.Qt import QTest, QTransform
from PyQt5 import QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from constants import *
import os
import time


class MainWindow(QMainWindow):
    def __init__(self, widget, parent = None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0,0,col10,row10)
        self.widget = widget
        self.setCentralWidget(self.widget)

class PhotoViewer(QWidget):
    def __init__(self, parent, photos, time_interval, dir):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet('background-color:black')
        self.setGeometry(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0,0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self._curr_img = 0
        self.images = photos
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_image)
        self.timer.start(time_interval * 1000)
        self.photo_timer = QTimer(self)
        self.photo_timer.timeout.connect(self.check_photos)
        self.photo_timer.start(5000)
        self.ddir = dir

    def check_photos(self):
        photos = os.listdir(self.ddir)
        self.images = [x for x in photos if x.endswith('.jpg') or x.endswith('.png') or x.endswith('.jpeg')]

    @property
    def curr_img(self):
        return self._curr_img

    @curr_img.setter
    def curr_img(self, value):
        if value >= len(self.images):
            self._curr_img = 0
        else:
            self._curr_img = value

    def next_image(self):
        self.curr_img += 1
        try:
            self.parent().change_slideshow(self.images[self.curr_img])
        except FileNotFoundError:
            self.check_photos()


class SmallScreen(QWidget):
    '''
    Esta clase representa la pantalla pequeña que se crea para poder volver al programa
    si esque así fuera necesario.
    '''
    def __init__(self, driver=None, parent = None, password = None, photos = False):
        super().__init__(parent)
        self.setWindowOpacity(0.05)
        self.setGeometry(col9, row9, col, row)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.browser = driver
        self.count = []
        self.password_editor = password
        self.photos = photos
        self.show()

    def mousePressEvent(self, event):
        if len(self.count) == 0:
            self.begin = time.time()
        self.count.append(1)
        if time.time() - self.begin > 10:
            self.count = [1]
            self.begin = time.time()
        if len(self.count) >= 5:
            self.count = []
            self.begin = time.time()
            self.password_editor.show()
            self.password_editor.function = self.go_back

    def go_back(self):
        self.close()
        if self.photos:
            self.browser.timer.stop()
            self.browser.close()
        elif self.browser:
            try:
                if isinstance(self.browser, QWidget):
                    self.browser.player.stop()
                    self.browser.video_widget.close()
                self.browser.close()
            except:
                self.browser.widget.load(QUrl("https://www.google.com"))
                self.browser.widget.close()
                self.browser.close()


class VideoScreen(QWidget):
    '''
    Esta clase representa el reproductor de videos del programa
    '''
    def __init__(self, ddir, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 0, col10, row10)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute( Qt.WA_NoSystemBackground, True)
        self.ddir = ddir
        self.clips = ["{}/{}".format(ddir,name) for name in os.listdir(str(ddir)) if name.endswith(".mp4") or name.endswith('.mkv')]
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.video_widget.setGeometry(0, 0, col10, row10)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.addMedia()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_videos)
        self.timer.start(10000)

    def check_videos(self):
        clips = ["{}/{}".format(self.ddir,name) for name in os.listdir(str(self.ddir)) if name.endswith(".mp4") or name.endswith('.mkv')]
        for clip in clips:
            if clip not in self.clips:
                self.playlist.addMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(clip)))
        self.clips = clips

    def addMedia(self):
        for clip in self.clips:
            self.playlist.addMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(clip)))


class BlockerWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(None)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.05)
        self.setGeometry(0,0,SCREEN_WIDTH, SCREEN_HEIGHT)

    def mousePressEvent(self, event):
        self.parent.hide()


class PasswordWindow(QWidget):
    def __init__(self, function, parent = None):
        super().__init__(parent)

        self.blocker = BlockerWindow(self)
        self.blocker.show()

        self.function = function
        self.setGeometry(col, row4, col8, row2 + row/2)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        self.label = QLabel("Ingrese una contraseña", self)
        self.label.setGeometry(col/2, row/3, col7, row/2)
        self.label.setFont(QFont("Sans", 25))

        self.editor = PasswordEditor(self)
        self.editor.setGeometry(col/2, row, col7, row/2)
        self.editor.setFont(QFont("Sans",25))

        self.boton = QPushButton("ACEPTAR", self)
        self.boton.setGeometry(col, row + 2 * row/3, col6, row/2)
        self.boton.clicked.connect(self.aceptar)
        self.boton.setFont(QFont("Sans", 25))
        self.boton.setStyleSheet("background-color: rgb(200, 200, 200); border-radius: 30px")

        self.password = None

        self.timer  = QTimer(self)
        self.timer.timeout.connect(self.reset)

    def aceptar(self):
        if self.password:
            if self.editor.text() == self.password:
                self.function()
                self.hide()
            else:
                self.hide()
        else:
            self.password = self.editor.text()
            self.editor.setText("")
            self.function()
            self.hide()

    def reset(self):
        self.editor.setText("")
        self.hide()

    def hide(self):
        self.timer.stop()
        self.blocker.hide()
        super().hide()

    def show(self):
        self.timer.start(5000)
        self.blocker.show()
        super().show()


class PasswordEditor(QLineEdit):

    def __init__(self, parent = None):
        super().__init__(parent)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.parent().timer.stop()
        self.parent().timer.start(5000)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.parent().timer.stop()
        self.parent().timer.start(5000)


class WebBrowser(QWebEngineView):
    def __init__(self, url, photos=False, parent=None, local=False):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.page().fullScreenRequested.connect(lambda request: request.accept())
        self.local = local
        if not local:
            self.url = url
            self.cute_url = self.url.replace("https://", "")
            self.cute_url = self.cute_url.replace("http://", "")
            self.current_url = None
            self.load(QUrl(self.url))
            self.show()
        else:
            local_url = QUrl.fromLocalFile(url)
            self.url = local_url
            self.current_url = None
            self.load(self.url)
        if not photos:
            self.urlChanged.connect(self.url_change)

    def url_change(self, e):
        if not self.local:
            self.load(QUrl(self.url))

    def load(self, url):
        if url.url() == self.current_url:
            pass
        else:
            self.current_url = url.url()
            super().load(url)
