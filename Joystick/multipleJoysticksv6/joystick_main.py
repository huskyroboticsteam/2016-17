from PyQt4 import QtGui
from joystick import Joystick
import sys
import sdl2.ext
from sdl_output import SDLInstance


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)  # app object needs to be declared once per program to make PyQt windows

    sdl_instance = SDLInstance()    # Initializes PySDL2 to read and store joystick input
    joysticks = []
    for joy_num in range(sdl2.SDL_NumJoysticks()):  # Runs once for every connected joystick
        joysticks.append(Joystick(sdl_instance, joy_num))

    # How to get data
    # joystick[JOYSTICK_NUM].get_joystick_axis(JOYSTICK_NUM, AXIS_NUM)

    exit(app.exec_())   # Tells PyQt to wait for the 'X' to be clicked to close
