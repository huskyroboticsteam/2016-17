from PyQt4 import QtGui
from joystick import Joystick
import sys


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)  # app object needs to be declared once per program to make PyQt windows

    js = Joystick()

    exit(app.exec_())   # Tells PyQt to wait for the 'X' to be clicked to close
