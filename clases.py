from PyQt5.QtGui import QPixmap, QTransform, QCursor, QIcon, QImage, QBrush, \
    QPalette, QFont
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QSize, Qt, QThread, \
    QCoreApplication, QUrl
from PyQt5.QtWidgets import QLabel, QWidget, QMainWindow, QApplication, \
    QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QProgressBar, QGroupBox, QFileDialog
from PyQt5.Qt import QTest, QTransform, QSound
from PyQt5 import QtMultimedia, QtMultimediaWidgets
from constants import *
import os
import time

class SmallScreen(QWidget):
    '''
    Esta clase representa la pantalla pequeña que se crea para poder volver al programa
    si esque así fuera necesario.
    '''
    def __init__(self, driver= None, parent = None):
        super().__init__(parent)
        self.setWindowOpacity(0.05)
        self.setGeometry(col9, row9, col, row)
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


class VideoScreen(QWidget):
    '''
    Esta clase representa el reproductor de videos del programa
    '''
    def __init__(self, ddir, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 0, col10, row10)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.clips = ["{}/{}".format(ddir,name) for name in os.listdir(str(ddir)) if name.endswith(".mp4")]
        self.video_widget = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self.video_widget)
        layout = QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        self.playlist = QtMultimedia.QMediaPlaylist()
        self.addMedia()
        self.playlist.setPlaybackMode(QtMultimedia.QMediaPlaylist.Loop)
        self.player.setPlaylist(self.playlist)

    def addMedia(self):
        for clip in self.clips:
            self.playlist.addMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(clip)))
