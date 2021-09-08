from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sqlite3

import dbClass


class ModifyWindow(object):
    def setupUi(self):
        self.msgbox = QMessageBox()
        self.msgbox.setStyleSheet("QMessageBox {background-color: white}")
        self.msgbox.setGeometry(850, 400, 200, 200)

        self.id = None
       
        self.modWindow = QtWidgets.QMainWindow()
        self.modWindow.resize(720, 450)
        self.modWindow.setMaximumSize(720, 450)
        self.modWindow.setMinimumSize(720, 450)
        self.modWindow.setWindowTitle("회원정보 수정")

        self.modCentral = QtWidgets.QWidget(self.modWindow)
        self.modCentral.setGeometry(0, 0, 720, 450)

        self.modStackedWidget = QtWidgets.QStackedWidget(self.modCentral)
        self.modStackedWidget.setGeometry(0, 0, 720, 450)
        self.modStackedWidget.setStyleSheet(
            "background-color: black;"
        )

        self.passwordCheck = QtWidgets.QWidget()

        self.modLogo = QtWidgets.QLabel(self.passwordCheck)
        self.modLogo.setGeometry(280, 20, 150, 80)
        self.modLogo.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(25)
        self.modLogo.setFont(font)
        self.modLogo.setStyleSheet(
            "color: red;"
            "background-color: black;"
        )
        self.modLogo.setAlignment(QtCore.Qt.AlignCenter)

        self.pwLabel = QtWidgets.QLabel(self.passwordCheck)
        self.pwLabel.setGeometry(170, 150, 150, 70)
        self.pwLabel.setStyleSheet(
            "background-color: black;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.pwLabel.setFont(font)
        self.pwLabel.setText("비밀번호")

        self.pwInput = QtWidgets.QLineEdit(self.passwordCheck)
        self.pwInput.setGeometry(330, 170, 200, 40)
        self.pwInput.setStyleSheet("background-color: white;")
        self.pwInput.setEchoMode(QtWidgets.QLineEdit.Password)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.pwInput.setFont(font)

        self.okBtn = QtWidgets.QPushButton(self.passwordCheck)
        self.okBtn.setGeometry(285, 300, 150, 70)
        self.okBtn.setStyleSheet(
            "background-color: red;"
            "color: white;"
            "border-radius: 3px;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.okBtn.setFont(font)
        self.okBtn.setText("확인")
        self.okBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.modStackedWidget.addWidget(self.passwordCheck)


        self.modifyPage = QtWidgets.QWidget()
        self.modifyPage.setStyleSheet(
            "background-color: white;"
        )

        self.modLogo2 = QtWidgets.QLabel(self.modifyPage)
        self.modLogo2.setGeometry(280, 20, 150, 80)
        self.modLogo2.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(25)
        self.modLogo2.setFont(font)
        self.modLogo2.setStyleSheet(
            "color: red;"
            "background-color: white;"
        )
        self.modLogo2.setAlignment(QtCore.Qt.AlignCenter)

        self.infoTitle = []
        self.titleName = ["비밀번호", "비밀번호 확인", "이름", "연락처"]
        for i in range(0, 4):
            label = QtWidgets.QLabel(self.modifyPage)
            label.setGeometry(140, 140 + i * 45, 150, 35)
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setFamily("맑은 고딕")
            label.setFont(font)
            label.setText(self.titleName[i])
            self.infoTitle.append(label)
            
        
        self.infoInput = []
        for i in range(0, 4):
            input = QtWidgets.QLineEdit(self.modifyPage)
            input.setGeometry(310, 140 + i * 45, 270, 35)
            input.setStyleSheet(
                "border-radius: 1px;"
                "border: 1px solid grey;"

            )
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("맑은 고딕")
            input.setFont(font)
            if i == 0 or i == 1:
                input.setMaxLength(12)
                input.setEchoMode(QtWidgets.QLineEdit.Password)
            else:
                input.setMaxLength(11)
    
            self.infoInput.append(input)


            self.cancelBtn = QtWidgets.QPushButton(self.modifyPage)
            self.cancelBtn.setGeometry(150, 350, 150, 70)
            self.cancelBtn.setStyleSheet(
                "border-radius: 4px;"
                "background-color: grey;"
                "color: white;"
            )
            font = QtGui.QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(14)
            self.cancelBtn.setFont(font)
            self.cancelBtn.setText("취소")
            self.cancelBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


            self.finModify = QtWidgets.QPushButton(self.modifyPage)
            self.finModify.setGeometry(400, 350, 150, 70)
            self.finModify.setStyleSheet(
                "border-radius: 4px;"
                "background-color: red;"
                "color: white;"
            )
            font = QtGui.QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(14)
            self.finModify.setFont(font)
            self.finModify.setText("수정")
            self.finModify.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

            self.modStackedWidget.addWidget(self.modifyPage)

    def okBtnClicked(self):
        pwValue = self.pwInput.text()
        if len(pwValue) == 0:
            self.msgbox.about(self.msgbox, "회원정보 수정", "비밀번호를 입력해 주세요.")

        else:
            conn = sqlite3.connect("UserDb.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM user WHERE id = '" + self.id + "';")
            data = cur.fetchall()

            if len(data) == 1:
                if str(data[0][1]) == pwValue:
                    self.infoInput[0].setText("")
                    self.infoInput[1].setText("")
                    self.infoInput[2].setText(str(data[0][2]))
                    self.infoInput[3].setText(str(data[0][3]))

                    self.modStackedWidget.setCurrentIndex(1)
                    
                
                else:
                    self.msgbox.warning(self.msgbox, '회원정보 수정', '비밀번호를 확인해 주세요.')
                    self.pwInput.setText("")

            else:
                self.msgbox.warning(self.msgbox, '회원정보 수정', '비밀번호를 확인해 주세요.')
                self.pwInput.setText("")

    def cancelClicked(self):
        for i in range(0, 4):
            self.infoInput[i].setText("")
        self.pwInput.setText("")
        self.modStackedWidget.setCurrentIndex(0)
        self.modWindow.close()

    def finModClicked(self):
        if len(self.infoInput[0].text()) == 0 or len(self.infoInput[2].text()) == 0 or len(self.infoInput[3].text()) == 0 or (self.infoInput[0].text() != self.infoInput[1].text()):
            self.msgbox.about(self.msgbox, "회원정보 수정", "입력하신 정보를 확인해 주세요.")
        else:
            choice = self.msgbox.question(self.msgbox, "회원정보 수정", "수정하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if choice == QMessageBox.Yes:
                conn = sqlite3.connect("UserDb.db")
                cur = conn.cursor()

                cur.execute("UPDATE user SET pwd = ? WHERE id = '" + self.id + "'", (self.infoInput[0].text(), ))
                conn.commit()
                cur.execute("UPDATE user SET nickname = ? WHERE id = '" + self.id + "'", (self.infoInput[2].text(), ))
                conn.commit()
                cur.execute("UPDATE user SET phone = ? WHERE id = '" + self.id + "'", (self.infoInput[3].text(), ))
                conn.commit()
                conn.close()
                self.msgbox.about(self.msgbox, "회원정보 수정", "수정되었습니다.")
                self.pwInput.setText("")

                self.modWindow.close()

            elif choice == QMessageBox.No:
                pass

    def setId(self, id):
        self.id = id
