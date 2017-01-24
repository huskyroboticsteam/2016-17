from PyQt4 import QtGui, QtCore, Qt


class Stop(QtGui.QPushButton):
    def __init__(self, Master=None):
        super(Stop, self).__init__(Master)

        self.setAutoFillBackground(True)

        p = self.palette()
        color = QtGui.QColor()
        color.setRgb(145, 44, 238, 255)
        p.setColor(self.backgroundRole(), color)
        p.setColor(self.foregroundRole(), color)
        self.setPalette(p)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        self.setText("Emergency Stop")
        self.setDisabled(True)

    def keyPressEvent(self, e):
        # If we have focus and press shift we will go to the next phase
        if self.hasFocus() and e.key() == QtCore.Qt.Key_Shift:
            self.setText("STOP!!!")

    def keyReleaseEvent(self, e):
        # If we release shift reset the text
        if e.key() == QtCore.Qt.Key_Shift:
            self.setText("Emergency Stop")

    def enterEvent(self, e):
        # Set focus on the stop button because of mouse rollover
        self.setDisabled(False)
        self.setFocus(1)

    def leaveEvent(self, e):
        # Reset text and set focus on some other arbitrary widget
        self.setText("Emergency Stop")
        self.nextInFocusChain().setFocus(7)





