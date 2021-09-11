from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import pafy
import youtube_dl


class Player:
    
    def __init__(self, ui):
        self.ui = ui
        self.videoCount = 0
        self.ui.exitBtn.clicked.connect(self.exitClicked)
        self.ui.addVideo.clicked.connect(self.addVideoEvent)
        self.videoList = []


    def exitClicked(self):
        self.ui.listTitle.setText("")

        self.ui.stackedWidget.setCurrentIndex(2)


    def addVideoEvent(self):
        url = "https://youtu.be/flGrDwKqUrQ"
        video = pafy.new(url)

        self.videoCount += 1
        newAdd = QtWidgets.QLabel(self.ui.videoListW)
        
        newAdd.setGeometry(0, 10 + 100 * (self.videoCount - 1), 170, 96)
        newAdd.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px"
        )
        newAdd.show()
        self.videoList.append(newAdd)
        
        

        