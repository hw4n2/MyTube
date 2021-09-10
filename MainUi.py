from os import X_OK
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys


class MainUi(object):
    
    def setupUi(self):
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(1600, 900)
        self.MainWindow.setMinimumSize(QtCore.QSize(1600, 900))
        self.MainWindow.setMaximumSize(QtCore.QSize(1600, 900))

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setGeometry(0, 0, 1600, 900)

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1600, 900))
        self.stackedWidget.setStyleSheet(
            "background-color: black;"
        )
#===============================================================================================
# login
#===============================================================================================
        self.loginPage = QtWidgets.QWidget()
        
        
        self.loginLogo = QtWidgets.QLabel(self.loginPage)
        self.loginLogo.setGeometry(QtCore.QRect(20, 10, 400, 150))
        self.loginLogo.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(60)
        self.loginLogo.setFont(font)
        self.loginLogo.setStyleSheet(
            "color: red;"
            "background-color: black;"
        )
        self.loginLogo.setAlignment(QtCore.Qt.AlignCenter)

        self.loginLabel = QtWidgets.QLabel(self.loginPage)
        self.loginLabel.setGeometry(QtCore.QRect(30, 600, 150, 50))
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(24)
        self.loginLabel.setFont(font)
        self.loginLabel.setStyleSheet(
            "color: white;"
            "background-color: black;"
        )

        self.idInput = QtWidgets.QLineEdit(self.loginPage)
        self.idInput.setGeometry(30, 670, 270, 55)
        self.idInput.setMaxLength(20)
        self.idInput.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        self.idInput.setFont(font)

        self.pwInput = QtWidgets.QLineEdit(self.loginPage)
        self.pwInput.setGeometry(30, 730, 270, 55)
        self.pwInput.setMaxLength(12)
        self.pwInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwInput.setStyleSheet(
            "background-color: white;"
            "border-radius: 2px;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        self.pwInput.setFont(font)

        self.loginButton = QtWidgets.QPushButton(self.loginPage)
        self.loginButton.setGeometry(310, 670, 170, 115)
        self.loginButton.setStyleSheet(
            "border-radius: 3px;"
            "background-color: red;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        self.loginButton.setFont(font)
        self.loginButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.gotoRegister = QtWidgets.QPushButton(self.loginPage)
        self.gotoRegister.setGeometry(405, 800, 70, 30)
        self.gotoRegister.setStyleSheet(
            "background-color: black;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        self.gotoRegister.setFont(font)
        self.gotoRegister.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.stackedWidget.addWidget(self.loginPage)

#===============================================================================================
# register
#===============================================================================================
        self.registerPage = QtWidgets.QWidget()
        self.registerPage.setStyleSheet(
            "background-color: white;"
        )
        
        self.regLogo = QtWidgets.QLabel(self.registerPage)
        self.regLogo.setGeometry(QtCore.QRect(20, 10, 400, 150))
        self.regLogo.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(60)
        self.regLogo.setFont(font)
        self.regLogo.setStyleSheet(
            "color: red;"
            "background-color: white;"
        )
        self.regLogo.setAlignment(QtCore.Qt.AlignCenter)

        self.divLine = QtWidgets.QLabel(self.registerPage)
        self.divLine.setGeometry(430, 30, 2, 800)
        self.divLine.setStyleSheet(
            "background-color: black;"
        )

        self.registerLabel = QtWidgets.QLabel(self.registerPage)
        self.registerLabel.setGeometry(900, 70, 200, 90)
        self.registerLabel.setStyleSheet(
            "background-color: white;"
            "color: black"
        )
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setFamily("맑은 고딕")
        self.registerLabel.setFont(font)

        self.infoTitle = []
        for i in range(0, 5):
            label = QtWidgets.QLabel(self.registerPage)
            label.setGeometry(630, 200 + 90 * i, 200, 70)
            font = QtGui.QFont()
            font.setPointSize(14)
            font.setFamily("맑은 고딕")
            label.setFont(font)
            self.infoTitle.append(label)
        
        self.infoInput = []
        for i in range(0, 5):
            input = QtWidgets.QLineEdit(self.registerPage)
            input.setGeometry(800, 215 + 90 * i, 500, 45)
            input.setStyleSheet(
                "border-radius: 1px;"
                "border: 1px solid grey;"

            )
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("맑은 고딕")
            input.setFont(font)
            if i == 1 or i == 2:
                input.setMaxLength(12)
                input.setEchoMode(QtWidgets.QLineEdit.Password)
            elif i == 0:
                input.setGeometry(800, 215 + 90 * i, 370, 45)
                input.setMaxLength(20)
            else:
                input.setMaxLength(11)
            if i == 2:
                input.setGeometry(800, 215 + 90 * i, 370, 45)
                input.setMaxLength(12)

            self.infoInput.append(input)

        self.isExistLabel = QtWidgets.QLabel(self.registerPage)
        self.isExistLabel.setGeometry(1180, 215, 125, 45)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.isExistLabel.setFont(font)

        self.isSameLabel = QtWidgets.QLabel(self.registerPage)
        self.isSameLabel.setGeometry(1180, 395, 125, 45)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.isSameLabel.setFont(font)
        
        self.cancelBtn = QtWidgets.QPushButton(self.registerPage)
        self.cancelBtn.setGeometry(800, 730, 200, 75)
        self.cancelBtn.setStyleSheet(
            "border-radius: 4px;"
            "background-color: grey;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.cancelBtn.setFont(font)
        self.cancelBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.registerBtn = QtWidgets.QPushButton(self.registerPage)
        self.registerBtn.setGeometry(1050, 730, 200, 75)
        self.registerBtn.setStyleSheet(
            "border-radius: 4px;"
            "background-color: red;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.registerBtn.setFont(font)
        self.registerBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.stackedWidget.addWidget(self.registerPage)

#===============================================================================================
# playlist
#===============================================================================================
        self.playlistPage = QtWidgets.QWidget()

        self.logoutBtn = QtWidgets.QPushButton(self.playlistPage)
        self.logoutBtn.setGeometry(-3, -3, 50, 50)
        self.logoutBtn.setStyleSheet(
            "background-color: white;"
            "border-radius: 4px;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(30)
        self.logoutBtn.setFont(font)
        self.logoutBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.mainLogo = QtWidgets.QLabel(self.playlistPage)
        self.mainLogo.setGeometry(QtCore.QRect(650, 0, 300, 150))
        self.mainLogo.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(50)
        self.mainLogo.setFont(font)
        self.mainLogo.setStyleSheet(
            "color: red;"
            "background-color: black;"
        )
        self.mainLogo.setAlignment(QtCore.Qt.AlignCenter)
        
        self.userIcon = QtWidgets.QLabel(self.playlistPage)
        self.userIcon.setGeometry(1360, 30, 60, 60)
        pixmap = QtGui.QPixmap("image\images.png")
        pixmap = pixmap.scaled(60, 60)
        self.userIcon.setPixmap(pixmap)

        self.idShowLabel = QtWidgets.QLabel(self.playlistPage)
        self.idShowLabel.setGeometry(1430, 25, 150, 25)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setFamily("맑은 고딕")
        self.idShowLabel.setFont(font)
        self.idShowLabel.setStyleSheet(
            "color: white;"
            "background-color: black;"
        )

        self.modifyInfoBtn = QtWidgets.QPushButton(self.playlistPage)
        self.modifyInfoBtn.setGeometry(1430, 60, 120, 30)
        self.modifyInfoBtn.setStyleSheet(
            "background-color: white;"
            "border-radius: 5px;"
            "color: black;"
        )
        self.modifyInfoBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        

        self.divline2 = QtWidgets.QLabel(self.playlistPage)
        self.divline2.setGeometry(20, 160, 1560, 2)
        self.divline2.setStyleSheet(
            "background-color: white;"
        )

        self.addListBtn = QtWidgets.QPushButton(self.playlistPage)
        self.addListBtn.setGeometry(1530, 170, 60, 60)
        self.addListBtn.setStyleSheet(
            "background-color: white;"
            "border-radius: 4px;"
        )
        font = QtGui.QFont()
        font.setPointSize(20)
        self.addListBtn.setFont(font)
        self.addListBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        
        self.listScroll = QtWidgets.QScrollArea(self.playlistPage)
        self.listScroll.setGeometry(45, 250, 1523, 605)
        self.listScroll.setStyleSheet(
            "background-color: black;"
        )

        self.listWidget = QtWidgets.QWidget(self.listScroll)
        self.listWidget.setGeometry(0, 0, 1500, 600)
        self.listWidget.setStyleSheet(
            "background-color: black;"
        )
        self.listScroll.setWidget(self.listWidget)
        

        self.stackedWidget.addWidget(self.playlistPage)

#===============================================================================================
# player
#===============================================================================================
        self.playerPage = QtWidgets.QWidget()

        self.divline3 = QtWidgets.QLabel(self.playerPage)
        self.divline3.setGeometry(1150, 0, 2, 900)
        self.divline3.setStyleSheet(
            "background-color: white;"
        )

        self.divline4 = QtWidgets.QLabel(self.playerPage)
        self.divline4.setGeometry(0, 750, 1150, 2)
        self.divline4.setStyleSheet(
            "background-color: white;"
        )

        self.exitBtn = QtWidgets.QPushButton(self.playerPage)
        self.exitBtn.setGeometry(-3, -3, 50, 50)
        self.exitBtn.setStyleSheet(
            "background-color: white;"
            "border-radius: 4px;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(30)
        self.exitBtn.setFont(font)
        self.exitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.curVideoTitle = QtWidgets.QLabel(self.playerPage)
        self.curVideoTitle.setGeometry(60, 0, 1030, 40)
        self.curVideoTitle.setStyleSheet(
            "background-color: black;"
            "color: white;"
        )
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(16)
        self.curVideoTitle.setFont(font)
        self.curVideoTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.curVideoTitle.setText("untitled")

        self.videoScroll = QtWidgets.QScrollArea(self.playerPage)
        self.videoScroll.setGeometry(1152, 30, 448, 900)
        self.videoScroll.setStyleSheet(
            "background-color: white;"
        )

        self.inScroll = QtWidgets.QWidget(self.videoScroll)
        self.inScroll.setGeometry(0, 0, 448, 900)
        self.inScroll.setStyleSheet(
            "background-color: black;"
        )
        self.videoScroll.setWidget(self.inScroll)

        self.listTitle = QtWidgets.QLabel(self.playerPage)
        self.listTitle.setGeometry(1152, 0, 448, 30)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        self.listTitle.setFont(font)
        self.listTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.listTitle.setStyleSheet(
            "background-color: black;"
            "color: white;"
        )

        self.playBtn = QtWidgets.QPushButton(self.playerPage)
        self.playBtn.setGeometry(10, 820, 60, 60)
        self.playBtn.setStyleSheet(
            "background-color: white;"
            "border-radius: 30px;"
        )
        self.playBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.controlBtnsL = []
        for i in range(0, 3):
            button = QtWidgets.QPushButton(self.playerPage)
            button.setGeometry(80 + 38 * i, 820, 30, 30)
            button.setStyleSheet(
                "background-color: white;"
                "border-radius: 15px;"
            )
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.controlBtnsL.append(button)

        self.controlBtnsR = []
        for i in range(0, 4):
            button = QtWidgets.QPushButton(self.playerPage)
            button.setGeometry(980 + 38 * i, 820, 30, 30)
            button.setStyleSheet(
                "background-color: white;"
                "border-radius: 15px;"
            )
            button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.controlBtnsR.append(button)

        self.playerLogo = QtWidgets.QLabel(self.playerPage)
        self.playerLogo.setGeometry(QtCore.QRect(470, 820, 150, 40))
        self.playerLogo.setText("MyTube")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        self.playerLogo.setFont(font)
        self.playerLogo.setStyleSheet(
            "color: red;"
            "background-color: black;"
        )
        self.playerLogo.setAlignment(QtCore.Qt.AlignCenter)
        

        self.stackedWidget.addWidget(self.playerPage)





        self.retranslateUi(self.MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.MainWindow.show()

    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyTube"))
        self.loginLabel.setText(_translate("MainWindow", "로그인"))
        self.idInput.setPlaceholderText(_translate("MainWindow", "아이디"))
        self.pwInput.setPlaceholderText(_translate("MainWindow", "비밀번호"))
        self.loginButton.setText(_translate("MainWindow", "로그인"))
        self.gotoRegister.setText(_translate("MainWindow", "회원가입"))
        self.registerLabel.setText(_translate("MainWindow", "회원가입"))
        title = ["아이디", "비밀번호", "비밀번호 확인", "이름", "연락처"]
        for i in range(0, 5):
            self.infoTitle[i].setText(_translate("MainWindow", title[i]))
        self.infoInput[0].setPlaceholderText(_translate("MainWindow", "아이디는 4자 이상 20자 이하입니다."))
        self.infoInput[1].setPlaceholderText(_translate("MainWindow", "비밀번호는 4자 이상 12자 이하입니다."))
        self.infoInput[2].setPlaceholderText(_translate("MainWindow", "비밀번호를 한번 더 입력해 주세요."))
        self.infoInput[3].setPlaceholderText(_translate("MainWindow", "이름을 입력해 주세요."))
        self.infoInput[4].setPlaceholderText(_translate("MainWindow", "숫자만 입력해 주세요."))
        self.cancelBtn.setText(_translate("MainWindow", "취소"))
        self.registerBtn.setText(_translate("MainWindow", "가입"))
        self.logoutBtn.setText(_translate("MainWindow", "⇦"))
        self.idShowLabel.setText(_translate("MainWindow", "아이디"))
        self.modifyInfoBtn.setText(_translate("MainWindow", "회원정보 수정"))
        self.addListBtn.setText(_translate("MainWindow", "➕"))
        self.exitBtn.setText(_translate("MainWindow", "⇦"))




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    test = MainUi()
    test.setupUi()
    test.stackedWidget.setCurrentIndex(2)

    sys.exit(app.exec_())