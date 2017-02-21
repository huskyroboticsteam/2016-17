from PyQt4 import QtGui, QtCore
import Bootstrap


class MainWindow(QtGui.QWidget):
    def __init__(self, width, height, fps, parent=None):
        super(MainWindow,self).__init__(parent)

        self.fps = fps
        self.map = Bootstrap.ImageWidget(width, height, fps)
        hbox = QtGui.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self.setSizePolicy(policy)

        hbox.addWidget(self.map)

        self.setLayout(hbox)

    def initialize(self, map_name):
        return Bootstrap.bootstrap_pygame(self.map, map_name, self.fps)
