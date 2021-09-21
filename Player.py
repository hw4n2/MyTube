from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pafy, urllib.request
import vlc

import SearchWindow, dbClass

 
class Player:
    
    def __init__(self, ui):
        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("QMessageBox {background-color: white}")
        self.msgbox.setGeometry(850, 400, 200, 200)

        self.id = None
        self.ui = ui
        self.ui.exitBtn.clicked.connect(self.exitClicked)
        self.ui.addVideo.clicked.connect(self.addVideoClicked)
        self.videoList = []
        self.titleList = []
        self.URL = []
        self.loadURL = []

        self.curList_index = -1
        self.curListTitle = ""

        self.search = SearchWindow.SearchWindow()
        self.search.searchBtn.mousePressEvent = lambda e: self.search.searchClicked(e)
        self.search.finBtn.mousePressEvent = lambda e: self.okClicked(e)
        self.search.finBtn.mouseReleaseEvent = lambda e: self.search.closeWindow(e)


        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
        self.mediaplayer.set_hwnd(self.ui.videoframe.winId())
        self.isPaused = False

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updatePosition)


    def exitClicked(self):
        self.ui.listTitle.setText("")
        self.ui.stackedWidget.setCurrentIndex(2)
        self.curList_index = -1
        self.loadURL.clear()

    def addVideoClicked(self):
        for i in range(0, len(self.search.videoList)):
            try:
                self.search.videoList[i].close()
                self.search.titleList[i].close()
                self.search.returnURL[i].close()
            except:
                pass

        self.search.videoList.clear()
        self.search.titleList.clear()
        self.search.returnURL.clear()
        

        self.search.searchEdit.setText("")
        self.search.searchWindow.show()

    def okClicked(self, e):
        self.URL = self.search.returnList()

        for i in range(0, len(self.URL)):
            if len(self.URL) >= 1 and i >= 1:
                self.ui.videoListW.setGeometry(0, 0, 425, self.ui.videoListW.height() + 130)
            self.loadURL.append(self.URL[i])

        for i in range(0, len(self.loadURL)):
            self.relocateVideo(i)

    def relocateVideo(self, index):
        if index == 0:
            for i in range(0, len(self.videoList)):
                self.videoList[i].close()
                self.titleList[i].close()
            self.videoList.clear()
            self.titleList.clear()
        

        
        if index >= 7:
            self.ui.videoListW.setGeometry(0, 0, 425, self.ui.videoListW.height() + 130)

        url = self.loadURL[index]
        video = pafy.new(url)
        thumbUrl = video.thumb
        thumbnail = urllib.request.urlopen(thumbUrl).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(thumbnail)
        pixmap = pixmap.scaled(170, 120)

        newVideo = QtWidgets.QLabel(self.ui.videoListW)
        newVideo.setGeometry(0, 10 + 125 * index, 170, 120)
        newVideo.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px"
        )
        newVideo.setPixmap(pixmap)

        newTitle = QtWidgets.QLabel(self.ui.videoListW)
        newTitle.setGeometry(170, 10 + 125 * index, 255, 120)
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

        self.videoList.append(newVideo)
        self.titleList.append(newTitle)

        

        newVideo.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        newTitle.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        deleteActionV = QAction("삭제", newVideo)
        deleteActionT = QAction("삭제", newTitle)
        newVideo.addAction(deleteActionV)
        newTitle.addAction(deleteActionT)
        v = newVideo
        t = newTitle
        u = url
        deleteActionV.triggered.connect(lambda: self.deleteClicked(v, t, u))
        deleteActionT.triggered.connect(lambda: self.deleteClicked(v, t, u))

        newVideo.mousePressEvent = lambda e, u: self.startVideo(e, u)
        newTitle.mousePressEvent = lambda e, u: self.startVideo(e, u)

        newVideo.show()
        newTitle.show()

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

    def clearWidget(self):
        for i in range(0, len(self.videoList)):
            self.videoList[0].close()
            self.titleList[0].close()
            del self.videoList[0]
            del self.titleList[0]

    def deleteClicked(self, video, title, url):
        for i in range(0, len(self.loadURL)):
            if self.loadURL[i] == url:
                index = i
        
        video.close()
        title.close()

        db = dbClass.UseDb()
        db.update(self.id, ["v" + str(index)], [None], "v" + str(index), url)

        self.msgbox.about(self.msgbox, "삭제", "삭제되었습니다.")

        
        del self.loadURL[index]
        del self.titleList[index]
        del self.videoList[index]


        db = dbClass.UseDb()
        data = db.select(self.id, ["*"], "listname", self.curListTitle)

        tempurl = []
        for k in range(0, len(data[0]) - 1):
            if data[0][k + 1] == None:
                continue
            tempurl.append(data[0][k + 1])


        for j in range(0, 10):
            if j < len(tempurl):
                db.update(self.id, ["v" + str(j)], [tempurl[j]], "listname", self.curListTitle)
            else:
                db.update(self.id, ["v" + str(j)], [None], "listname", self.curListTitle)

        for i in range(0, len(self.loadURL)):
            self.relocateVideo(i)

    def setId(self, id):
        self.id = id

    def startVideo(self, e, url):
        if self.mediaplayer.is_playing():
            self.mediaplayer.stop()

        if url != None:
            self.media = self.instance.media_new(self.loadURL[0])
            self.mediaplayer.set_media(self.media)

        else:
            self.media = self.instance.media_new(url)
            self.mediaplayer.set_media(self.media)

        self.media.parse()
        self.ui.curVideoTitle.setText(self.media.get_meta(0))
        
        self.mediaplayer.play()
        self.timer.start()

    def play(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.play()
            self.isPaused = False


    def pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.isPaused = True

        else:
            pass
    
    def stop(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.stop()
            self.timer.stop()

        else:
            pass
        
    def setVolume(self, volume):
        self.mediaplayer.audio_set_volume(volume)

    def setPosition(self, position):
        self.mediaplayer.set_position(position / 1000.0)

    def updatePosition(self):
        self.ui.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            self.timer.stop()