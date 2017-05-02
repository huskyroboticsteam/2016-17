from PyQt4 import QtGui
import sys
import arm_widget

if __name__ == '__main__':

        app = QtGui.QApplication(sys.argv)

        window = QtGui.QMainWindow()

        # List of urls to play in the UI, width and height of each video container
        ui = arm_widget.arm_widget()

        window.setCentralWidget(ui)
        window.resize(500, 500)

        window.show()

        # Start the UI loop
        app.exec_()