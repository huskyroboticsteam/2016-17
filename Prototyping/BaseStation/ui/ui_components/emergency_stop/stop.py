from PyQt4 import QtGui, QtCore, Qt


class Stop(QtGui.QWidget):
    def __init__(self, Master=None):
        super(Stop, self).__init__(Master)

        self.setAutoFillBackground(True)

        p = self.palette()
        color = QtGui.QColor()
        color.setRgb(145, 44, 238, 255)
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        self.label = QtGui.QLabel()
        self.label.setText("Emergency Stop")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        p = self.label.palette()
        color = QtGui.QColor()
        color.setRgb(255, 215, 0, 255)
        p.setColor(self.label.foregroundRole(), color)
        self.label.setPalette(p)

        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.label)

        self.setLayout(vbox)

    def keyPressEvent(self, e):
        # If we have focus and press shift we will go to the next phase
        if self.hasFocus() and e.key() == QtCore.Qt.Key_Shift:
            self.label.setText("STOP!!!")

    def keyReleaseEvent(self, e):
        # If we release shift reset the text
        if e.key() == QtCore.Qt.Key_Shift:
            self.label.setText("Emergency Stop")

    def enterEvent(self, e):
        # Set focus on the stop button because of mouse rollover
        self.setFocus(1)

    def leaveEvent(self, e):
        # Reset text and set focus on some other arbitrary widget
        self.label.setText("Emergency Stop")
        self.nextInFocusChain().setFocus(7)





