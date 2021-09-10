from PyQt5 import QtCore
from PyQt5.QtWidgets import *

import dbClass, Animation, MainLogic

 
class Register:

    def __init__(self, ui):
        self.ui = ui
        self.existCheck = 0
        self.sameCheck = 0
        self.ui.infoInput[0].textChanged.connect(self.idCheck)
        self.ui.infoInput[2].textChanged.connect(self.isSame)

        self.ui.registerBtn.clicked.connect(self.registButtonClicked)
        self.ui.cancelBtn.clicked.connect(self.back)

        self.newAni = Animation.Ani()
        registerBtnAni = QtCore.QPropertyAnimation(self.ui.registerBtn, b"geometry")
        self.ui.registerBtn.enterEvent = lambda event, a = registerBtnAni, x = self.ui.registerBtn.x(), y = self.ui.registerBtn.y(), w = self.ui.registerBtn.width(), h = self.ui.registerBtn.height(): self.newAni.expandAnimation(event, a, x, y, w, h, self.ui.registerBtn)
        self.ui.registerBtn.leaveEvent = lambda event, a = registerBtnAni, x = self.ui.registerBtn.x(), y = self.ui.registerBtn.y(), w = self.ui.registerBtn.width(), h = self.ui.registerBtn.height(): self.newAni.minimizeAnimation(event, a, x, y, w, h, self.ui.registerBtn)

        cancelBtnAni = QtCore.QPropertyAnimation(self.ui.cancelBtn, b"geometry")
        self.ui.cancelBtn.enterEvent = lambda event, a = cancelBtnAni, x = self.ui.cancelBtn.x(), y = self.ui.cancelBtn.y(), w = self.ui.cancelBtn.width(), h = self.ui.cancelBtn.height(): self.newAni.expandAnimation(event, a, x, y, w, h, self.ui.cancelBtn)
        self.ui.cancelBtn.leaveEvent = lambda event, a = cancelBtnAni, x = self.ui.cancelBtn.x(), y = self.ui.cancelBtn.y(), w = self.ui.cancelBtn.width(), h = self.ui.cancelBtn.height(): self.newAni.minimizeAnimation(event, a, x, y, w, h, self.ui.cancelBtn)

        

    def idCheck(self):
        self.existCheck = 0
        self.idValue = self.ui.infoInput[0].text()

        if len(self.idValue) < 4:
            self.ui.isExistLabel.setText("4자 이상")
            self.ui.isExistLabel.setStyleSheet("color: red;")
            self.existCheck = 2

        else:
            db = dbClass.UseDb()
            data = db.select("user", ["id"], "id", self.idValue)
            
            if len(data) != 0:
                self.ui.isExistLabel.setText("사용중인 아이디")
                self.ui.isExistLabel.setStyleSheet("color: red;")
                self.existCheck = 0
            else:
                self.ui.isExistLabel.setText("사용 가능")
                self.ui.isExistLabel.setStyleSheet("color: green;")
                self.existCheck = 1
            
    def isSame(self):
        self.sameCheck = 0
        pw = self.ui.infoInput[1].text()
        pwRe = self.ui.infoInput[2].text()
        if pw == pwRe:
            self.ui.isSameLabel.setText("일치")
            self.ui.isSameLabel.setStyleSheet("color: green;")
            self.sameCheck = 1

        else:
            self.ui.isSameLabel.setText("불일치")
            self.ui.isSameLabel.setStyleSheet("color: red;")
            self.sameCheck = 0

    def registButtonClicked(self):

        if self.existCheck == 0:
            QMessageBox.warning(self.ui.registerPage, '회원가입', '이미 사용중인 아이디입니다.', QMessageBox.Ok, QMessageBox.Ok)
        
        elif self.existCheck == 2:
            QMessageBox.warning(self.ui.registerPage, '회원가입', '아이디는 4글자 이상입니다.', QMessageBox.Ok, QMessageBox.Ok)

        

        else:    
            pwValue = self.ui.infoInput[1].text()
            nameValue = self.ui.infoInput[3].text()
            phoneValue = self.ui.infoInput[4].text()
            

            if len(pwValue) == 0 or len(nameValue) == 0 or len(phoneValue) == 0:
                QMessageBox.warning(self.ui.registerPage, '회원가입', '모든 정보를 입력해 주세요.', QMessageBox.Ok, QMessageBox.Ok)
            
            elif len(pwValue) < 4:
                QMessageBox.warning(self.ui.registerPage, '회원가입', '비밀번호는 4자리 이상입니다.')

            elif self.sameCheck == 0:
                QMessageBox.warning(self.ui.registerPage, '회원가입', '비밀번호가 일치하지 않습니다.', QMessageBox.Ok, QMessageBox.Ok)
                
            else:
                db = dbClass.UseDb()
                db.insert("user", ["id", "pwd", "nickname", "phone"], [self.idValue, pwValue, nameValue, phoneValue])
                
                QMessageBox.about(self.ui.registerPage, '회원가입', '회원가입이 완료되었습니다.\n로그인해 주세요.')
                for i in range(0, 5):
                    self.ui.infoInput[i].setText("")
                self.ui.isExistLabel.setText("")
                self.ui.isSameLabel.setText("")
                self.ui.idInput.setFocus()

                
                self.ui.stackedWidget.setCurrentIndex(0)
                        
    def back(self):
        for i in range(0, 5):
            self.ui.infoInput[i].setText("")
        self.ui.isExistLabel.setText("")
        self.ui.isSameLabel.setText("")
        self.ui.idInput.setFocus()
        self.ui.stackedWidget.setCurrentIndex(0)
        
