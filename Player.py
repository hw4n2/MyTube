

class Player:
    
    def __init__(self, ui):
        self.ui = ui
        self.ui.exitBtn.clicked.connect(self.exitClicked)


    def exitClicked(self):
        self.ui.listTitle.setText("")

        self.ui.stackedWidget.setCurrentIndex(2)