import sys

from PyQt4 import QtGui, QtCore

import qt_bootstrap


class MainWindow(QtGui.QMainWindow):
    def __init__(self, width, height, wid, parent=None):
        super(MainWindow,self).__init__(parent)
        mainwid = QtGui.QWidget(self)

        self.wid = wid

        vbox = QtGui.QVBoxLayout(self);
        vbox.addWidget(wid)
        self.label = QtGui.QLabel(self)
        self.label.setText("TEST")
        vbox.addWidget(self.label)

        mainwid.setLayout(vbox)


        self.setCentralWidget(mainwid)
        self.resize(width, height)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(2000)

    def update(self):

        self.label.setText("Joystick A " + self.wid.data)


# Bootstrap the PyGame widget to the PyQt4 widget and use it to make the UI
def createUI(width, height):

    app=QtGui.QApplication(sys.argv)

    # Create the frame with the refresh rate that we will put PyGame in
    # In a real UI environment will need to place these frames in a class object to be retrieved after UI creation
    image = qt_bootstrap.ImageWidget(width, height, 120)
    #image2 = qt_bootstrap.ImageWidget(width, height, 100)

    w = MainWindow(width, height, image)
    w.show()
    #w2 = MainWindow(width, height, image2)
    #w2.move(300, 0)
    #w2.show()

    # Must bootstrap PyGame after the UI has been shown
    qt_bootstrap.bootstrap_pygame(image)

    # Start the main application loop
    app.exec_()