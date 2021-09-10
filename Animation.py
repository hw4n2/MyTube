from PyQt5 import QtCore
from PyQt5.QtWidgets import QGraphicsOpacityEffect

class Ani:
   
    def LogoFadeIn(self, widget):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)

        self.animation = QtCore.QPropertyAnimation(self.effect, b"opacity")
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setDuration(1500)
        self.animation.start()

    def expandAnimation(self, event, ani, x, y, w, h, obj):
        ani.setStartValue(QtCore.QRect(x, y, w, h)) 
        ani.setEndValue(QtCore.QRect(x - 2, y - 2, w + 4, h + 4))
        ani.setDuration(30)
        ani.start()

        
        # if obj.iconSize() == QtCore.QSize(160, 160):
        #     obj.setIconSize(QtCore.QSize(168, 168))

        # elif obj.iconSize() == QtCore.QSize(120, 120):
        #     obj.setIconSize(QtCore.QSize(128, 128))

        # elif obj.iconSize() == QtCore.QSize(60, 60):
        #     obj.setIconSize(QtCore.QSize(68, 68))

    def minimizeAnimation(self, event, ani, x, y, w, h, obj):
        ani.setStartValue(QtCore.QRect(x - 2, y - 2, w + 4, h + 4))
        ani.setEndValue(QtCore.QRect(x, y, w, h))
        ani.setDuration(30)
        ani.start()

        # if obj.iconSize() == QtCore.QSize(168, 168):
        #     obj.setIconSize(QtCore.QSize(160, 160))

        # elif obj.iconSize() == QtCore.QSize(128, 128):
        #     obj.setIconSize(QtCore.QSize(120, 120))

        # elif obj.iconSize() == QtCore.QSize(68, 68):
        #     obj.setIconSize(QtCore.QSize(60, 60))

        