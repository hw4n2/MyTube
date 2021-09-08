from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sqlite3

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
        # self.ui.addListBtn.clicked.connect()

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

    def setId(self, id):
        self.id = id