import Map
import sys
from PyQt4 import QtGui

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()

    # Updates IPs every 20 seconds.
    ui = Map.Map("UW")

    window.setCentralWidget(ui)
    window.resize(300, 500)

    window.show()

    app.aboutToQuit.connect(quit)
    app.exec_()
