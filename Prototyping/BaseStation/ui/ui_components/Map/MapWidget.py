from PyQt4 import QtGui, QtCore
import Bootstrap


class MainWindow(QtGui.QWidget):
    def __init__(self, width, height, fps, parent=None):
        super(MainWindow,self).__init__(parent)

        self.map = Bootstrap.ImageWidget(width, height, fps)
        hbox = QtGui.QHBoxLayout()

        hbox.addWidget(self.map)

        self.setLayout(hbox)

    def initialize(self):
        Bootstrap.bootstrap_pygame(self.map)