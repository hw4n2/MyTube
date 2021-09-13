from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pafy, urllib.request
from youtubesearchpython import VideosSearch

class SearchWindow(object):
    
    def __init__(self):
        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("QMessageBox {background-color: white}")
        self.msgbox.setGeometry(850, 400, 200, 200)

        self.videoList = []
        self.titleList = []

        self.returnURL = []
        self.searchWindow = QtWidgets.QMainWindow()
        self.searchWindow.resize(1400, 800)
        self.searchWindow.setMaximumSize(1400, 800)
        self.searchWindow.setMinimumSize(1400, 800)
        self.searchWindow.setWindowTitle("영상 검색")
        
        self.centralWidget = QtWidgets.QWidget(self.searchWindow)
        self.centralWidget.setGeometry(0, 0, 1400, 800)
        self.centralWidget.setStyleSheet(
            "background-color: black;"
        )
        
        self.searchScr = QtWidgets.QScrollArea(self.centralWidget)
        self.searchScr.setGeometry(190, 100, 1000, 600)
        self.searchScr.setStyleSheet(
            "background-color: white;"
        )
        self.searchScr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.inscr = QtWidgets.QWidget(self.searchScr)
        self.inscr.setGeometry(0, 0, 1000, 1300)
        self.inscr.setStyleSheet(
            "background-color: black;"
        )

        self.searchScr.setWidget(self.inscr)

        self.searchEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.searchEdit.setGeometry(400, 30, 480, 50)
        self.searchEdit.setStyleSheet(
            "background-color: white;"
            "border: 2px solid grey;"
            "color: black;"
        )
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("맑은 고딕")
        self.searchEdit.setFont(font)

        self.searchBtn = QtWidgets.QPushButton(self.centralWidget)
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchBtn.setGeometry(885, 30, 100, 50)
        self.searchBtn.setStyleSheet(
            "background-color: red;"
            "color: white;"
            "border-radius: 2px;"
            
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("맑은 고딕")
        self.searchBtn.setFont(font)
        self.searchBtn.setText("검색")

        self.finBtn = QtWidgets.QPushButton(self.centralWidget)
        self.finBtn.setGeometry(650, 720, 100, 50)
        self.finBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.finBtn.setStyleSheet(
            "background-color: red;"
            "color: white;"
            "border-radius: 2px;"
        )
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("맑은 고딕")
        self.finBtn.setFont(font)
        self.finBtn.setText("확인")

    

    def searchClicked(self):
        search = VideosSearch(self.searchEdit.text(), limit=5)
        searchList = search.result()
        resultList = []
        for i in range(0, 5):
            resultList.append(searchList['result'][i]['link'])

        self.videoList = []
        self.titleList = []
        self.displayVideoEvent(resultList)
        
    def displayVideoEvent(self, resultList):
        for i in range(0, 5):
            url = resultList[i]
            video = pafy.new(url)
            thumbUrl = video.thumb
            thumbnail = urllib.request.urlopen(thumbUrl).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(thumbnail)
            pixmap = pixmap.scaled(340, 220)

            newVideo = QtWidgets.QLabel(self.inscr)
            newVideo.setGeometry(10, 10 + 225 * i, 340, 220)
            newVideo.setStyleSheet(
                "background-color: black;"
                "border-radius: 2px"
            )
            newVideo.setPixmap(pixmap)
            newVideo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            newVideo.setText(url)


            newTitle = QtWidgets.QLabel(self.inscr)
            newTitle.setGeometry(350, 10 + 225 * i, 620, 220)
            newTitle.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            newTitle.setStyleSheet(
                "background-color: black;"
                "color: white;"
            )
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("맑은 고딕")
            newTitle.setFont(font)
            
            finalTitle = self.cutTitle(video)
            newTitle.setText(finalTitle)

            newVideo.mousePressEvent = lambda e, v = newVideo, l = newTitle: self.videoClicked(e, v, l)
            newTitle.mousePressEvent = lambda e, v = newVideo, l = newTitle: self.videoClicked(e, v, l)

            newVideo.show()
            newTitle.show()
            self.videoList.append(newVideo)
            self.titleList.append(newTitle)
            

    def cutTitle(self,video):
        titleString = video.title
        cutStr = []
        for i in range(0, len(titleString) + 1):
            if len(titleString) > 40:
                try:
                    cutStr.append(titleString[:40])
                    titleString = titleString[40:]  
                except:
                    cutStr.append(titleString)
            else: 
                cutStr.append(titleString)
                break
        
        finalTitle = ""
        for i in range(0, len(cutStr)):
            finalTitle += cutStr[i] + "\n"

        finalTitle += "\n" + video.author
        return finalTitle

    def videoClicked(self, e, video, label):
        index = None
        for i in range(0, len(self.returnURL)):
            if self.returnURL[i] == video.text():
                index = i

        if index == None:
            choice = self.msgbox.question(self.msgbox, "장바구니", "추가하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if choice == QMessageBox.No:
                pass
            
            elif choice == QMessageBox.Yes:
                label.setStyleSheet(
                    "background-color: grey;"
                )
                self.returnURL.append(video.text())
        
        elif index != None:
            choice = self.msgbox.question(self.msgbox, "장바구니", "취소하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            
            if choice == QMessageBox.No:
                pass
            
            elif choice == QMessageBox.Yes:
                label.setStyleSheet(
                    "background-color: black;"
                    "color: white;"
                )
                del self.returnURL[index]

    def closeWindow(self, e):
        self.searchWindow.close()

    def returnList(self):
        return self.returnURL

