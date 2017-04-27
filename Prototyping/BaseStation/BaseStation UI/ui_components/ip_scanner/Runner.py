import IPCheckerLayout
import sys
from PyQt4 import QtGui


def quit():
    ui.worker_thread.quit()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()

    maps = {"192.168.1.6": "first", "192.168.1.44": "second", "192.168.1.45": "third", "192.168.1.47": "fourth"}

    lel = {}

    for i in range(150, 200):
        lel["192.168.1." + str(i)] = "192.168.1." + str(i)

    # Updates IPs every 20 seconds.
    ui = IPCheckerLayout.IPList(lel, 5000)

    window.setCentralWidget(ui)
    window.resize(300, 500)

    window.show()

    app.aboutToQuit.connect(quit)
    app.exec_()
