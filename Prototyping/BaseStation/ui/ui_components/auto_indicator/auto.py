from PyQt4 import QtGui, QtCore


class Auto(QtGui.QLabel):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setText("")

        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)

    def toggle_ui(self, on):
        if on:
            self.setText("")
        else:
            self.setText("AUTO")
