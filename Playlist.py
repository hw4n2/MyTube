from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sqlite3

from sip import delete

import ModifyWindow

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
        self.playList = []
        self.titleList = []
        self.listCount = 0
        
        self.modWin = ModifyWindow.ModifyWindow()
        self.modWin.setupUi()
        self.modWin.okBtn.clicked.connect(self.modWin.okBtnClicked)
        self.modWin.pwInput.returnPressed.connect(self.modWin.okBtnClicked)
        self.modWin.cancelBtn.clicked.connect(self.modWin.cancelClicked)
        self.modWin.finModify.clicked.connect(self.modWin.finModClicked)

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
        self.playList.append(newList)

        newTitle.setGeometry(newList.x(), newList.y() + 160, 285, 30)
        newTitle.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: black;"
        )
        newTitle.setText("새 재생목록 " + str(self.listCount))
        newTitle.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily("맑은 고딕")
        newTitle.setFont(font)
        self.titleList.append(newTitle)

        if 260 * ((self.listCount - 1) // 4 + 1) >= self.ui.listWidget.height():
            self.ui.listWidget.setGeometry(0, 0, 1500, self.ui.listWidget.height() + 300)

        newList.mousePressEvent = lambda e, n = newTitle.text(): self.listClicked(e, n)
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


    def listClicked(self, e, name):
        if e.button() == QtCore.Qt.LeftButton:
            self.ui.stackedWidget.setCurrentIndex(3)
            self.ui.listTitle.setText(name)
        
        elif e.button() == QtCore.Qt.RightButton:
            pass
                
    def deleteClicked(self, list, title):
        index = self.playList.index(list)
        list.close()
        title.close()
        self.listCount -= 1

        del self.playList[index]
        del self.titleList[index]

        self.relocateWidget()

    def relocateWidget(self):
        for i in range(0, len(self.playList)):
            self.playList[i].close()
            self.titleList[i].close()

        for i in range(0, len(self.playList)):
            self.playList[i].setGeometry(90 + (i % 4) * 345, 50 + (i // 4) * 260, 285, 160)
            self.titleList[i].setGeometry(self.playList[i].x(), self.playList[i].y() + 160, 285, 30)
            self.playList[i].show()
            self.titleList[i].show()

    def titleModifyEvent(self, title):
        index = self.titleList.index(title)
        self.titleList[index].setEnabled(True)
        self.titleList[index].setStyleSheet(
            "background-color: white;"
            "color: black;"
        )

    def modifyReturnPressed(self, title):
        index = self.titleList.index(title)
        self.titleList[index].setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: black;"
        )
        self.titleList[index].setText(self.titleList[index].text())
        self.titleList[index].setEnabled(False)

    def setId(self, id):
        self.id = id



    
        
