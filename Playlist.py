from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import pafy, urllib.request
 
import ModifyWindow, Player, dbClass, Animation

class Playlist:
    
    def __init__(self, ui):
        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("QMessageBox {background-color: white}")
        self.msgbox.setGeometry(850, 400, 200, 200)
        
        self.ui = ui
        self.id = None
        self.ui.logoutBtn.clicked.connect(self.logoutClicked)
        self.ui.modifyInfoBtn.clicked.connect(self.modifyClicked)
        self.ui.addListBtn.clicked.connect(self.addClicked)
        self.ui.saveBtn.clicked.connect(self.saveClicked)
        self.playList = []
        self.titleList = []
        self.listCount = 0

        self.saveBtnList = []

        self.player = Player.Player(self.ui)
        
        self.modWin = ModifyWindow.ModifyWindow()
        self.modWin.setupUi()
        self.modWin.okBtn.clicked.connect(self.modWin.okBtnClicked)
        self.modWin.pwInput.returnPressed.connect(self.modWin.okBtnClicked)
        self.modWin.cancelBtn.clicked.connect(self.modWin.cancelClicked)
        self.modWin.finModify.clicked.connect(self.modWin.finModClicked)

        self.newAni = Animation.Ani()
        logoutBtnAni = QtCore.QPropertyAnimation(self.ui.logoutBtn, b"geometry")
        self.ui.logoutBtn.enterEvent = lambda event, a = logoutBtnAni, x = self.ui.logoutBtn.x(), y = self.ui.logoutBtn.y(), w = self.ui.logoutBtn.width(), h = self.ui.logoutBtn.height(): self.newAni.expandAnimation(event, a, x, y, w, h, self.ui.logoutBtn)
        self.ui.logoutBtn.leaveEvent = lambda event, a = logoutBtnAni, x = self.ui.logoutBtn.x(), y = self.ui.logoutBtn.y(), w = self.ui.logoutBtn.width(), h = self.ui.logoutBtn.height(): self.newAni.minimizeAnimation(event, a, x, y, w, h, self.ui.logoutBtn)

        modifyBtnAni = QtCore.QPropertyAnimation(self.ui.modifyInfoBtn, b"geometry")
        self.ui.modifyInfoBtn.enterEvent = lambda event, a = modifyBtnAni, x = self.ui.modifyInfoBtn.x(), y = self.ui.modifyInfoBtn.y(), w = self.ui.modifyInfoBtn.width(), h = self.ui.modifyInfoBtn.height(): self.newAni.expandAnimation(event, a, x, y, w, h, self.ui.modifyInfoBtn)
        self.ui.modifyInfoBtn.leaveEvent = lambda event, a = modifyBtnAni, x = self.ui.modifyInfoBtn.x(), y = self.ui.modifyInfoBtn.y(), w = self.ui.modifyInfoBtn.width(), h = self.ui.modifyInfoBtn.height(): self.newAni.minimizeAnimation(event, a, x, y, w, h, self.ui.modifyInfoBtn)

        addBtnAni = QtCore.QPropertyAnimation(self.ui.addListBtn, b"geometry")
        self.ui.addListBtn.enterEvent = lambda event, a = addBtnAni, x = self.ui.addListBtn.x(), y = self.ui.addListBtn.y(), w = self.ui.addListBtn.width(), h = self.ui.addListBtn.height(): self.newAni.expandAnimation(event, a, x, y, w, h, self.ui.addListBtn)
        self.ui.addListBtn.leaveEvent = lambda event, a = addBtnAni, x = self.ui.addListBtn.x(), y = self.ui.addListBtn.y(), w = self.ui.addListBtn.width(), h = self.ui.addListBtn.height(): self.newAni.minimizeAnimation(event, a, x, y, w, h, self.ui.addListBtn)


    def logoutClicked(self):
        choice = self.msgbox.question(self.msgbox, "로그아웃", "로그아웃하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.ui.idShowLabel.setText("")
            self.ui.idInput.setText("")
            self.ui.pwInput.setText("")
            self.ui.idInput.setFocus()
            self.ui.stackedWidget.setCurrentIndex(0)
        elif choice == QMessageBox.No:
            pass

    def modifyClicked(self):
        self.modWin.setId(self.id)
        self.modWin.pwInput.setText("")
        self.modWin.modStackedWidget.setCurrentIndex(0)
        self.modWin.modWindow.show()

    def addClicked(self): 
        self.listCount += 1
        newList = QtWidgets.QLabel(self.ui.listWidget)
        newTitle = QtWidgets.QLineEdit(self.ui.listWidget)
        
        newList.setGeometry(90 + ((self.listCount - 1) % 4) * 345, 50 + ((self.listCount - 1) // 4) * 260, 285, 160)
        newList.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px"
        )
        self.playList.append([])
        self.playList[len(self.playList) - 1].append(newList)

        newTitle.setGeometry(newList.x(), newList.y() + 160, 285, 30)
        newTitle.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: black;"
        )

        db = dbClass.UseDb()
        data = db.select(self.id, ["listname"], None, "")

        for i in range(0, 100):
            count = 0
            for j in range(0, len(data)):
                if data[j][0] == "새 재생목록 " + str(i):
                    break
                
                else:
                    count += 1
                
            if count == len(data):
                newTitle.setText("새 재생목록 " + str(i))
                break

                    

        newTitle.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("맑은 고딕")
        newTitle.setFont(font)
        newTitle.setMaxLength(14)
        self.titleList.append(newTitle)

        if 260 * ((self.listCount - 1) // 4 + 1) >= self.ui.listWidget.height():
            self.ui.listWidget.setGeometry(0, 0, 1500, self.ui.listWidget.height() + 300)

        newList.mousePressEvent = lambda e, list = newList, title = newTitle: self.listClicked(e, list, title)
        newTitle.returnPressed.connect(lambda : self.modifyReturnPressed(newTitle))

        newList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        deleteAction = QAction("삭제", newList)
        modifyAction = QAction("이름 수정", newList)
        newList.addAction(deleteAction)
        newList.addAction(modifyAction)
        deleteAction.triggered.connect(lambda: self.deleteClicked(newList, newTitle))
        modifyAction.triggered.connect(lambda: self.titleModifyEvent(newTitle))

        db = dbClass.UseDb()
        db.insert(self.id, ["listname"], [newTitle.text()])

        newList.show()
        newTitle.show()

    def listClicked(self, e, list, title):
        if e.button() == QtCore.Qt.LeftButton:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.listTitle.setText(title.text())

            for i in range(0, len(self.playList)):
                if self.playList[i][0] == list:
                    index = i
                    break
            
            self.player.curListTitle = self.titleList[index].text()
            self.loadFromData()
            
            
            if len(self.playList[index]) != 1:
                self.player.loadURL.clear()
                for i in range(0, len(self.playList[index]) - 1):
                    self.player.loadURL.append(self.playList[index][i + 1])

                self.player.curList_index = index
                for i in range(0, len(self.player.loadURL)):
                    self.player.relocateVideo(i)
                self.player.startVideo(None, "nourl")
                self.player.replayToggle = False
                self.player.shuffleToggle = False

            else:
                self.player.curList_index = index
                self.player.clearWidget()
                self.msgbox.about(self.msgbox, "영상 추가", "재생목록이 비었습니다.")
                
        
        elif e.button() == QtCore.Qt.RightButton:
            pass
                
    def deleteClicked(self, list, title):
        for i in range(0, len(self.playList)):
            if self.playList[i][0] == list:
                index = i
        
        list.close()
        title.close()
        self.listCount -= 1

        db = dbClass.UseDb()
        db.delete(self.id, "listname", self.titleList[index].text())


        del self.playList[index]
        del self.titleList[index]

        self.relocateWidget()

    def relocateWidget(self):
        for i in range(0, len(self.playList)):
            self.playList[i][0].close()
            self.titleList[i].close()

        for i in range(0, len(self.playList)):
            self.playList[i][0].setGeometry(90 + (i % 4) * 345, 50 + (i // 4) * 260, 285, 160)
            self.titleList[i].setGeometry(self.playList[i][0].x(), self.playList[i][0].y() + 160, 285, 30)
            self.playList[i][0].show()
            self.titleList[i].show()

    def titleModifyEvent(self, title):
        index = self.titleList.index(title)
        self.titleList[index].setEnabled(True)
        self.titleList[index].setStyleSheet(
            "background-color: white;"
            "color: black;"
        )

        self.tempTitle = self.titleList[index].text()

    def modifyReturnPressed(self, title):
        db = dbClass.UseDb()
        data = db.select(self.id, ["listname"], None, "")

        count = 0
        for i in range(0, len(data)):
            if data[i][0] == title.text():
                break
            
            else:
                count += 1
            
        if count == len(data):
            index = self.titleList.index(title)
            self.titleList[index].setStyleSheet(
                "background-color: black;"
                "color: white;"
                "border: black;"
            )
            self.titleList[index].setText(self.titleList[index].text())
            self.titleList[index].setEnabled(False)

            
            db.update(self.id, ["listname"], [self.titleList[index].text()], "listname", self.tempTitle)
            self.tempTitle = ""

        else:
            self.msgbox.about(self.msgbox, "이름 수정", "이미 존재하는 재생목록명입니다.")
            
    def setId(self, id):
        self.id = id

    def saveClicked(self):
        if len(self.player.URL) != 0:
            index = self.player.curList_index
            db = dbClass.UseDb()
            data = db.select(self.id, ["*"], "listname", self.titleList[index].text())

            tempurl = []
            for k in range(0, len(data[0]) - 1):
                if data[0][k + 1] == None:
                    continue
                tempurl.append(data[0][k + 1])

            for i in range(0, len(self.player.URL)):
                tempurl.append(self.player.URL[i])
                self.playList[index].append(self.player.URL[i])

            for j in range(0, 10):
                if j < len(tempurl):
                    db.update(self.id, ["v" + str(j)], [tempurl[j]], "listname", self.titleList[index].text())
                else:
                    db.update(self.id, ["v" + str(j)], [None], "listname", self.titleList[index].text())


            for i in range(0, len(self.player.loadURL)):
                self.player.relocateVideo(i)
                
            self.player.URL.clear()
            self.player.search.returnURL.clear()


            
            self.msgbox.about(self.msgbox, "저장", "저장 완료")
            
        else:
            self.msgbox.about(self.msgbox, "저장", "변경사항이 없습니다.")

    def loadFromData(self):
        for i in range(0, len(self.titleList)):
            self.titleList[i].close()
            self.playList[i][0].close()

        db = dbClass.UseDb()
        data = db.select(self.id, ["*"], None, ".")
        self.titleList.clear()
        self.playList.clear()

        self.listCount = 0
        self.loadedTitle = []
        for i in range(0, len(data)):
            self.loadedTitle.append(data[i][0])
            self.loadList(i, data)

        self.player.setId(self.id)

    def loadList(self, index, data):
        self.listCount += 1
        newList = QtWidgets.QLabel(self.ui.listWidget)
        newTitle = QtWidgets.QLineEdit(self.ui.listWidget)
        
        newList.setGeometry(90 + (index % 4) * 345, 50 + (index // 4) * 260, 285, 160)
        newList.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px"
        )
        self.playList.append([])
        self.playList[len(self.playList) - 1].append(newList)
        for i in range(0, len(data[index]) - 1):
            if data[index][i + 1] == None:
                continue
            self.playList[len(self.playList) - 1].append(data[index][i + 1])

        if data[index][1] != None:
            url = data[index][1]
            video = pafy.new(url)
            thumbUrl = video.thumb
            thumbnail = urllib.request.urlopen(thumbUrl).read()
            pixmap = QtGui.QPixmap()
            pixmap.loadFromData(thumbnail)
            pixmap = pixmap.scaled(285, 210)
            newList.setPixmap(pixmap)

        newTitle.setGeometry(newList.x(), newList.y() + 160, 285, 30)
        newTitle.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: black;"
        )
        newTitle.setText(self.loadedTitle[index])
        newTitle.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("맑은 고딕")
        newTitle.setFont(font)
        newTitle.setMaxLength(14)
        self.titleList.append(newTitle)

        if 260 * (index // 4 + 1) >= self.ui.listWidget.height():
            self.ui.listWidget.setGeometry(0, 0, 1500, self.ui.listWidget.height() + 300)

        newList.mousePressEvent = lambda e, list = newList, title = newTitle: self.listClicked(e, list, title)
        newTitle.returnPressed.connect(lambda : self.modifyReturnPressed(newTitle))

        newList.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        deleteAction = QAction("삭제", newList)
        modifyAction = QAction("이름 수정", newList)
        newList.addAction(deleteAction)
        newList.addAction(modifyAction)
        deleteAction.triggered.connect(lambda: self.deleteClicked(newList, newTitle))
        modifyAction.triggered.connect(lambda: self.titleModifyEvent(newTitle))

        

        newList.show()
        newTitle.show()
