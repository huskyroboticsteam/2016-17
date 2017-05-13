from PyQt4 import QtCore, QtGui
import sdl2.ext


class SDLInstance:

    # Initialises PySDL2 and the variables to store the joystick data
    def __init__(self):
        self.joysticks = []
        self.joystick_axis = []
        self.joystick_ball = []
        self.joystick_hat = []
        self.joystick_button = []

    # Takes the joystick input and stores in variables
    def update_sdl2(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.joystick_axis[event.jaxis.which][event.jaxis.axis] = event.jaxis.value
                # print self.joystick_axis

            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.joystick_ball[event.jball.which][event.jball.ball] = [event.jball.xrel, event.jball.yrel]
                # print self.joystick_ball

            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.joystick_hat[event.jhat.which] = event.jhat.value
                # print self.joystick_hat

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.joystick_button[event.jbutton.which][event.jbutton.button] = event.jbutton.state
                # print self.joystick_button

            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.joystick_button[event.jbutton.which][event.jbutton.button] = event.jbutton.state
                # print self.joystick_button

            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                # Reconnect isn't working
                self.joysticks.append(sdl2.SDL_JoystickOpen(event.jdevice.which))

                added_joystick = len(self.joysticks) - 1

                axis_num = sdl2.SDL_JoystickNumAxes(self.joysticks[added_joystick])
                self.joystick_axis.append([])
                for j in range(axis_num):
                    self.joystick_axis[added_joystick].append(0)  # [axis1, axis2, axis2, ...]

                ball_num = sdl2.SDL_JoystickNumBalls(self.joysticks[added_joystick])
                self.joystick_ball.append([])
                for j in range(ball_num):
                    self.joystick_ball[added_joystick].append([0, 0])   # [[x, y]]

                hat_num = sdl2.SDL_JoystickNumHats(self.joysticks[added_joystick])
                for j in range(hat_num):
                    self.joystick_hat.append(0)  # [[direction]]

                button_num = sdl2.SDL_JoystickNumButtons(self.joysticks[added_joystick])
                self.joystick_button.append([])
                for j in range(button_num):
                    self.joystick_button[added_joystick].append(0)  # [button1, button2, button3, ...]

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                sdl2.SDL_JoystickClose(self.joysticks[event.jdevice.which])


class ReceiveData(QtGui.QWidget):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, parent=None):
        QtGui.QWidget.__init__(self, parent)  # Initialize PyQt widget
        self.sdl_instance = sdl_instance

    # Runs every cycle and updates the input from the joystick
    def update_input(self):
        self.sdl_instance.update_sdl2()


class Joystick(QtGui.QWidget):
    def __init__(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
            print "Couldn't initiate joystick(s)."
        else:
            self.sdl_instance = SDLInstance()    # Initializes PySDL2 to read and stores joystick input

            self.joystick_axis = self.sdl_instance.joystick_axis
            self.joystick_ball = self.sdl_instance.joystick_ball
            self.joystick_hat = self.sdl_instance.joystick_hat
            self.joystick_button = self.sdl_instance.joystick_button

            self.rd = ReceiveData(self.sdl_instance)

    def start(self):
        # Ties window refresh to joystick refresh
        QtGui.QWidget.__init__(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rd.update_input)
        timer.timeout.connect(self.update)
        timer.start(1000 / 120)  # Updates 120 times per second

    def update(self):
        self.joystick_axis = self.sdl_instance.joystick_axis
        self.joystick_ball = self.sdl_instance.joystick_ball
        self.joystick_hat = self.sdl_instance.joystick_hat
        self.joystick_button = self.sdl_instance.joystick_button

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)  # app object needs to be declared once per program to make PyQt windows

    js = Joystick()
    js.start()

    window = QtGui.QDialog()
    window.show()
    sys.exit(app.exec_())   # Waits for the 'X' to be clicked to close
