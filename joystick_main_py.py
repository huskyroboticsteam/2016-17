import sys
from window_py import *
from PyQt4 import QtGui, QtCore

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    sdl_instance = SDLInstance()

    did = DisplayInputData(sdl_instance)     # PyQt window that displays output
    jp = JoystickPosition(sdl_instance)    # PyQt window that displays the joysticks position
    rp = RoverPosition(sdl_instance)    # PyQt window that displays the rovers position

    main_app = MainApplication(did.update_l2, jp.update, rp.update)

    qtimer = QtCore.QTimer(did)

    rp.show()   # Makes the PyQt window visible
    jp.show()   # Makes the PyQt window visible
    did.show()   # Makes the PyQt window visible

    main_app.start_timer()

    exit(app.exec_())   # Tells PyQt to wait for the 'X' to be clicked to close