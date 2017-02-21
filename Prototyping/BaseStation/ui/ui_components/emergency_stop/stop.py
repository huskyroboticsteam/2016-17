from PyQt4 import QtGui, QtCore

"""
The emergency stop button for the rover.
Button presses are locked until the shift button is pressed.
"""


class Stop(QtGui.QPushButton):
    def __init__(self, Master=None):
        super(Stop, self).__init__(Master)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.setSizePolicy(policy)

        self.setAutoFillBackground(True)

        # Make the button purple
        p = self.palette()
        color = QtGui.QColor()
        color.setRgb(145, 44, 238, 255)
        p.setColor(self.backgroundRole(), color)
        p.setColor(self.foregroundRole(), color)
        self.setPalette(p)

        # Make the button text big and bold
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)

        self.setText("Emergency Stop")
        self.setDisabled(True)

    # If we are focused and we press shift, change button text
    # Overrides parent method
    def keyPressEvent(self, e):
        # If we have focus and press shift we will go to the next phase
        if self.hasFocus() and e.key() == QtCore.Qt.Key_Shift:
            self.setText("STOP!!!")

    # If we release shift then change the stop text to normal
    # Overrides parent method
    def keyReleaseEvent(self, e):
        # If we release shift reset the text
        if e.key() == QtCore.Qt.Key_Shift:
            self.setText("Emergency Stop")

    # If we roll over the button set focus on it
    # Overrides parent method
    def enterEvent(self, e):
        # Set focus on the stop button because of mouse rollover
        self.setDisabled(False)
        self.setFocus(1)

    # If we leave the button area set focus anywhere else
    # Overrides parent method
    def leaveEvent(self, e):
        # Reset text and set focus on some other arbitrary widget
        self.setText("Emergency Stop")
        self.nextInFocusChain().setFocus(7)





