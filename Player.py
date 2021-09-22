from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pafy, urllib.request
import vlc
import random

import SearchWindow, dbClass

 
class Player():
    
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

        self.timer = QtCore.QTimer(self.ui.videoframe)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUi)

        self.ui.positionslider.sliderMoved.connect(self.setPosition)
        self.ui.volumeslider.valueChanged.connect(self.setVolume)
        self.ui.playBtn.clicked.connect(self.play)
        self.ui.controlBtnsL[0].clicked.connect(self.pause)
        self.ui.controlBtnsL[1].clicked.connect(self.stop)
        self.ui.controlBtnsL[2].clicked.connect(self.minimize)
        self.ui.controlBtnsR[0].clicked.connect(self.replay)
        self.ui.controlBtnsR[1].clicked.connect(self.shuffle)

        self.miniWindow = QDialog()
        self.miniWindow.resize(200, 80)
        self.replayToggle = False
        self.shuffleToggle = False



    def exitClicked(self):
        self.ui.listTitle.setText("")
        self.ui.stackedWidget.setCurrentIndex(2)
        self.curList_index = -1
        self.loadURL.clear()
        self.mediaplayer.stop()

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

        newVideo.mousePressEvent = lambda e, u = url: self.startVideo(e, u)
        newTitle.mousePressEvent = lambda e, u = url: self.startVideo(e, u)

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

        if not "youtube" in url:
            video = pafy.new(self.loadURL[0])
            best = video.getbest()
            media = self.instance.media_new(best.url)
            self.mediaplayer.set_media(media)

            try:
                self.nextURL = self.loadURL[1]
            except:
                self.nextURL = None
            

        else:
            video = pafy.new(url)
            best = video.getbest()
            media = self.instance.media_new(best.url)
            self.mediaplayer.set_media(media)
            
            index = self.loadURL.index(url)
            try:
                self.nextURL = self.loadURL[index + 1]
            except:
                self.nextURL = None



        self.ui.curVideoTitle.setText(video.title)
        self.duration = video.duration
        self.ui.playtime.setText("00:00:00/" + self.duration)
        
        self.mediaplayer.play()
        self.timer.start()

    def play(self):
        if not self.mediaplayer.is_playing():
            self.mediaplayer.play()

    def setNext(self):
        self.mediaplayer.stop()
        
        if self.replayToggle == False and self.shuffleToggle == False and self.nextURL != None:
            video = pafy.new(self.nextURL)
            best = video.getbest()
            media = self.instance.media_new(best.url)
            self.mediaplayer.set_media(media)
            index = self.loadURL.index(self.nextURL)
            self.ui.curVideoTitle.setText(video.title)
            self.mediaplayer.play()

            try:
                self.nextURL = self.loadURL[index + 1]
            except:
                self.nextURL = None

        elif self.replayToggle == True:
            self.mediaplayer.play()

        elif self.shuffleToggle == True:
            index = random.randint(0, len(self.loadURL) - 1)
            video = pafy.new(self.loadURL[index])
            best = video.getbest()
            media = self.instance.media_new(best.url)
            self.mediaplayer.set_media(media)
            self.ui.curVideoTitle.setText(video.title)
            self.mediaplayer.play()

    def pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()

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

    def updateUi(self):
        if self.mediaplayer.get_position() >= 0.999:
            self.setNext()

        self.ui.positionslider.setValue(self.mediaplayer.get_position() * 1000.0)
        curms = self.mediaplayer.get_time()
        cursec = curms // 1000

        hr = cursec // 3600
        remainder = cursec % 3600
        if hr < 10:
            _hr = "0" + str(int(hr))
        else:
            _hr = str(int(hr))

        min = remainder // 60
        remainder = remainder % 60
        if min < 10:
            _min = "0" + str(int(min))
        else:
            _min = str(int(min))

        sec = remainder
        if sec < 10:
            _sec = "0" + str(int(sec))
        else:
            _sec = str(int(sec))

        self.ui.playtime.setText(_hr + ":" + _min + ":" + _sec + "/" + self.duration)

    def replay(self):
        if self.shuffleToggle == False:
            if self.replayToggle == False:
                self.replayToggle = True
                self.ui.controlBtnsR[0].setToolTip("반복재생 끄기")

            elif self.replayToggle == True:
                self.replayToggle = False
                self.ui.controlBtnsR[0].setToolTip("반복재생 켜기")


        else:
            self.msgbox.about(self.msgbox, "반복재생", "셔플을 먼저 꺼 주세요.")

    def shuffle(self):
        if self.replayToggle == False:
            if self.shuffleToggle == False:
                self.shuffleToggle = True
                self.ui.controlBtnsR[1].setToolTip("셔플 끄기")


            elif self.shuffleToggle == True:
                self.shuffleToggle = False
                self.ui.controlBtnsR[1].setToolTip("셔플 켜기")


        else:
            self.msgbox.about(self.msgbox, "셔플", "반복재생을 먼저 꺼 주세요.")


    def minimize(self):
        self.dialogBtn = []
        image = ["image\playBtn", "image\pause.jpg", "image\stop.jpg", "image\max.jpg"]
        for i in range(0, 4):
            button = QtWidgets.QPushButton(self.miniWindow)
            button.setGeometry(8 + 48 * i, 20, 40, 40)
            button.setStyleSheet(
                "border-radius: 20px;"
            )
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            pixmap = QtGui.QPixmap(image[i])
            button.setIcon(QtGui.QIcon(pixmap))
            button.setIconSize(QtCore.QSize(40, 40))
            self.dialogBtn.append(button)
        
        self.dialogBtn[0].clicked.connect(self.play)
        self.dialogBtn[1].clicked.connect(self.pause)
        self.dialogBtn[2].clicked.connect(self.stop)
        self.dialogBtn[3].clicked.connect(self.exit_min)

        
        
        self.miniWindow.show()
        self.ui.MainWindow.hide()

    
    def exit_min(self):
        self.miniWindow.close()
        self.ui.MainWindow.show()

        

        