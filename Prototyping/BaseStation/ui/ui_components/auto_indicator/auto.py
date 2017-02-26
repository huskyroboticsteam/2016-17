from PyQt4 import QtGui


class Auto(QtGui.QLabel):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setText("")

    def toggle_ui(self, on):
        if on:
            self.setText("")
        else:
            self.setText("AUTO")