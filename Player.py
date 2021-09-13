from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pafy,urllib.request

import Searching


class Player:
    
    def __init__(self, ui):
        self.ui = ui
        self.videoCount = 0
        self.ui.exitBtn.clicked.connect(self.exitClicked)
        self.ui.addVideo.clicked.connect(self.addVideoClicked)
        self.videoList = []
        self.titleList = []
        self.URL = []

        self.search = Searching.SearchWindow()
        self.search.searchBtn.clicked.connect(self.search.searchClicked)
        self.search.finBtn.mousePressEvent = lambda e: self.setVideos(e)
        self.search.finBtn.mouseReleaseEvent = lambda e: self.search.closeWindow(e)

    def exitClicked(self):
        self.ui.listTitle.setText("")
        self.ui.stackedWidget.setCurrentIndex(2)

    def addVideoClicked(self):
        for i in range(0, len(self.search.videoList)):
            self.search.videoList[i].close()
            self.search.titleList[i].close()

        self.search.videoList = []
        self.search.titleList = []
        self.search.returnURL = []
        

        self.search.searchEdit.setText("")
        self.search.searchWindow.show()


    def setVideos(self, e):
        self.URL = self.search.returnList()

        for i in range(0, len(self.URL)):
            if len(self.URL) >= 7 and i >= 7:
                self.ui.videoListW.setGeometry(0, 0, 425, self.ui.videoListW.height() + 130)

            url = self.URL[i]
            video = pafy.new(url)
            thumbUrl = video.thumb
            thumbnail = urllib.request.urlopen(thumbUrl).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(thumbnail)
            pixmap = pixmap.scaled(170, 120)

            self.videoCount += 1

            newVideo = QtWidgets.QLabel(self.ui.videoListW)
            newVideo.setGeometry(0, 10 + 125 * (self.videoCount - 1), 170, 120)
            newVideo.setStyleSheet(
                "background-color: white;"
                "border-radius: 2px"
            )
            newVideo.setPixmap(pixmap)

            newTitle = QtWidgets.QLabel(self.ui.videoListW)
            newTitle.setGeometry(170, 10 + 125 * (self.videoCount - 1), 255, 120)
            newTitle.setStyleSheet(
                "background-color: black;"
                "color: white;"
            )
            font = QtGui.QFont()
            font.setPointSize(9)
            font.setFamily("맑은 고딕")
            newTitle.setFont(font)
            
            finalTitle = self.cutTitle(video)
            newTitle.setText(finalTitle)

            newVideo.show()
            newTitle.show()
            self.videoList.append(newVideo)
            self.titleList.append(newTitle)

    def cutTitle(self,video):
        titleString = video.title
        cutStr = []
        for i in range(0, len(titleString) + 1):
            if len(titleString) > 20:
                try:
                    cutStr.append(titleString[:20])
                    titleString = titleString[20:]  
                except:
                    cutStr.append(titleString)
            else: 
                cutStr.append(titleString)
                break
        
        finalTitle = ""
        for i in range(0, len(cutStr)):
            finalTitle += cutStr[i] + "\n"

        finalTitle += video.author
        return finalTitle