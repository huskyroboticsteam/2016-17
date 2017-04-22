from PyQt4 import QtCore, QtGui
from sdl_output import SDLInstance
import sdl2.ext


class ReceiveData(QtGui.QWidget):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, joy_num, parent=None):
        QtGui.QWidget.__init__(self, parent)  # Initialize PyQt widget
        self.joy_num = joy_num
        self.sdl_instance = sdl_instance

    # Runs every cycle and updates the input from the joystick
    def update_input(self):
        self.sdl_instance.update_sdl2(self.joy_num)


class Joystick(QtGui.QWidget):
    def __init__(self):
        self.sdl_instance = SDLInstance()    # Initializes PySDL2 to read and stores joystick input

        self.joy_num = sdl2.SDL_NumJoysticks()
        self.sdl_instance.init_joy_vars(self.joy_num)
        self.rd = ReceiveData(self.sdl_instance, self.joy_num)

        # Ties window refresh to joystick refresh
        QtGui.QWidget.__init__(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.rd.update_input)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 / 120)  # Updates 120 times per second

    def update(self):
        self.joystick_axis = self.sdl_instance.joystick_axis
        self.joystick_ball = self.sdl_instance.joystick_ball
        self.joystick_hat = self.sdl_instance.joystick_hat
        self.joystick_button = self.sdl_instance.joystick_button
