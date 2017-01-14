from PyQt4 import QtGui
import sys
import MapWidget

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()

    # Updates IPs every 20 seconds.
    ui = MapWidget.MainWindow(500, 200, 120)

    window.setCentralWidget(ui)
    window.resize(500, 200)

    window.show()

    ui.initialize()

    app.exec_()