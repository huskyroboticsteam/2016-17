from PyQt4 import QtGui

class Stop(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Stop, self).__init__(parent)

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.drawRect()

