from PyQt4 import QtCore, QtGui


class ReceiveData(QtGui.QWidget):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, joy_num, parent=None):
        QtGui.QWidget.__init__(self, parent)  # Initialize PyQt widget
        self.joy_num = joy_num
        self.window_width, self.window_length = 200, 200
        self.setGeometry(100 + 250 * self.joy_num, 200, self.window_width,
                         self.window_length)  # Set window dimensions (x, y, w, h)
        title = "Joystick " + str(self.joy_num) + " Data"
        self.setWindowTitle(title)
        self.layout = QtGui.QVBoxLayout(self)
        self.sdl_instance = sdl_instance
        # Sets the background color to black
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

    # Runs every cycle and updates the input from the joystick
    def update_input(self):
        self.sdl_instance.update_sdl2(self.joy_num)


class Joystick(QtGui.QWidget):
    def __init__(self, sdl_instance, joy_num):
        self.sdl_instance = sdl_instance

        self.rd = ReceiveData(self.sdl_instance, joy_num)
        self.rd.show()

        QtGui.QWidget.__init__(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rd.update_input)
        timer.start(1000 / 120)  # Updates 120 times per second

    def get_joystick_axis(self, joy_num):
        # while True:
        #     print self.sdl_instance.joystick_axis[joy_num]
        return self.sdl_instance.joystick_axis[joy_num]
