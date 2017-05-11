from PyQt4 import QtGui, QtCore


class Stop(QtGui.QPushButton):

    """
    The emergency stop button for the rover.
    Button presses are locked until the shift button is pressed.
    """

    stopEvent = QtCore.pyqtSignal()

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

    def mousePressEvent(self, e):
        """
        If shift is held and we click, we emit signal
        Overrides parent method
        :param e: A PyQT MouseEvent object
        :return: Emits empty signal
        """

        super(Stop, self).mousePressEvent(e)
        if self.text().compare("STOP!!!") == 0:
            self.stopEvent.emit()

    def keyPressEvent(self, e):
        """
        If we are focused and we press shift, change button text
        Overrides parent method
        :param e: A PyQT KeyEvent object
        :return: None
        """

        super(Stop, self).keyPressEvent(e)
        # If we have focus and press shift we will go to the next phase
        if self.hasFocus() and e.key() == QtCore.Qt.Key_Shift:
            self.setText("STOP!!!")

    def keyReleaseEvent(self, e):
        """
        If we release shift then change the stop text to normal
        Overrides parent method
        :param e: A PyQT KeyEvent object
        :return: None
        """

        super(Stop, self).keyReleaseEvent(e)
        # If we release shift reset the text
        if e.key() == QtCore.Qt.Key_Shift:
            self.setText("Emergency Stop")





