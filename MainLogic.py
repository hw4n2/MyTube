import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *

import MainUi, Register, Playlist, Player, Animation, dbClass

class ProgramStart:
    
    def __init__(self, ui):
        self.ui = ui
        self.newRegister = Register.Register(self.ui)
        self.newPlaylist = Playlist.Playlist(self.ui)
        self.newPlayer = Player.Player(self.ui)
        self.newAni = Animation.Ani()

        
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.loginButton.clicked.connect(self.login)
        self.ui.idInput.returnPressed.connect(self.login)
        self.ui.pwInput.returnPressed.connect(self.login)

        self.ui.gotoRegister.clicked.connect(self.register)

        self.id = None

        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("QMessageBox {background-color: white}")
        self.msgbox.setGeometry(850, 400, 200, 200)

    def login(self):
        self.id = self.ui.idInput.text()
        pwValue = self.ui.pwInput.text()

        db = dbClass.UseDb()
        data = db.select1Db('user', 'pwd', 'id', self.id)
    
        if len(self.id) == 0 or len(pwValue) == 0:
            self.msgbox.warning(self.msgbox, '로그인', '아이디 또는 비밀번호를 입력해 주세요', QMessageBox.Ok, QMessageBox.Ok) 

        elif len(data) == 1:
            if str(data[0][0]) == pwValue:
                self.ui.stackedWidget.setCurrentIndex(2)
                self.ui.idShowLabel.setText(self.id)
                self.newPlaylist.setId(self.id)
            
            else:
                self.msgbox.warning(self.msgbox, '로그인', '아이디 또는 비밀번호를 확인해 주세요.', QMessageBox.Ok, QMessageBox.Ok)

        else:
            self.msgbox.warning(self.msgbox, '로그인', '아이디 또는 비밀번호를 확인해 주세요.', QMessageBox.Ok, QMessageBox.Ok)

    def register(self):
        self.ui.stackedWidget.setCurrentIndex(1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    ui = MainUi.MainUi()
    ui.setupUi()

    newPro = ProgramStart(ui)

    sys.exit(app.exec_())