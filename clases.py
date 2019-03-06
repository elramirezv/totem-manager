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


class VideoScreen(QtWidgets.QWidget):
    '''
    Esta clase representa el reproductor de videos del programa
    '''
    def __init__(self, layout, parent = None):
        super().__init__(parent)
        self.setGeometry(0, 0, col10, row10)
        self.current_video = QtMultimediaWidgets.QVideoWidget()
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setVideoOutput(self.current_video)
        self.layout = layout
        self.layout.addWidget(self.current_video)
        self.player.mediaStatusChanged.connect(self.handleMediaStateChanged)


    def addMedia(self):
        ddir = QFileDialog.getExistingDirectory(self)
        video_files = ["videos/{}".format(name) for name in os.listdir(str(ddir))]
        for video in videos_files:
            video_path = os.path.abspath(video)
            self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(video_path)))

    # def handlePositionChanged(self, pos):
    #     if (0 <= self._index < len(self._clips) and
    #         pos > self._clips[self._index][1] and
    #         self.player.state() == QtMultimedia.QMediaPlayer.PlayingState):
    #         self.playNext()
    #
    #
    # def handleMediaStateChanged(self, state):
    #     if state == QtMultimedia.QMediaPlayer.LoadedMedia:
    #         self.playNext()
