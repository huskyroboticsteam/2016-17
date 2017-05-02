import stop
import sys
from PyQt4 import QtGui

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()

    ui = stop.Stop()

    vbox = QtGui.QVBoxLayout()
    wid = QtGui.QWidget()

    vbox.addWidget(ui)
    wid.setLayout(vbox)

    window.setCentralWidget(wid)
    window.resize(300, 300)

    window.show()

    app.exec_()