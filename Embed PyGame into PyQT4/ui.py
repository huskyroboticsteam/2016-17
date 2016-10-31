from PyQt4 import QtGui
import sys
import qt_bootstrap


class MainWindow(QtGui.QMainWindow):
    def __init__(self, width, height, wid, parent=None):
        super(MainWindow,self).__init__(parent)

        self.setCentralWidget(wid)
        self.resize(width, height)


# Bootstrap the PyGame widget to the PyQt4 widget and use it to make the UI
def createUI(width, height):

    app=QtGui.QApplication(sys.argv)

    # Create the frame with the refresh rate that we will put PyGame in
    # In a real UI environment will need to place these frames in a class object to be retrieved after UI creation
    image = qt_bootstrap.ImageWidget(width, height, 60)

    w = MainWindow(width, height, image)
    w.show()

    # Must bootstrap PyGame after the UI has been shown
    qt_bootstrap.bootstrap_pygame(image)

    # Start the main application loop
    app.exec_()