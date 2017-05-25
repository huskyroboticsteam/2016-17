from PyQt4 import QtCore, QtGui
import sdl2
import sdl2.ext


class MapJoysticks(QtGui.QDialog):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, parent=None):
        QtGui.QDialog.__init__(self, parent)  # Initialize PyQt widget
        self.x, self.y = 100, 200
        self.window_width, self.window_length = 500, 300
        self.setGeometry(self.x, self.y, self.window_width, self.window_length)  # Set window dimensions (x, y, w, h)
        self.setWindowTitle("Map Joystick")
        self.sdl_instance = sdl_instance
        self.main = QtGui.QVBoxLayout(self)
        self.instruction_layout = QtGui.QVBoxLayout()
        self.main.addLayout(self.instruction_layout)
        self.instruction_layout.addWidget(QtGui.QLabel("Click a button and then press any button on a joystick to map it"))
        self.button_box = None

    def create_h_box(self, joy_num):
        h_layout = QtGui.QHBoxLayout()
        for i in range(joy_num):
            layout = self.create_v_box(str(i + 1))
            h_layout.addLayout(layout)
        return h_layout

    def create_v_box(self, name):
        layout = QtGui.QVBoxLayout()
        button = QtGui.QPushButton("Joystick Number " + name + " is mapped to index: " + str())
        layout.addWidget(button)
        button.released.connect(self.update_button(button, name))
        return layout

    def update_button(self, button, name):
        def update_button():
            joy_num = self.set_joystick_index()
            self.sdl_instance.joystick_control[int(name) - 1] = joy_num
            button.setText("Joystick Number " + name + " is mapped to index: " + str(joy_num))
        return update_button

    def set_joystick_index(self):
        while True:
            for event in sdl2.ext.get_events():
                if event.jbutton.state == 1:
                    return event.jdevice.which

    def update(self):
        joy_num = sdl2.SDL_NumJoysticks()
        self.sdl_instance.joystick_control = []
        for i in range(joy_num):
            self.sdl_instance.joystick_control.append(0)

        b = self.instruction_layout.itemAt(1)

        if b is not None:
            self.clearLayout(b)
            self.instruction_layout.removeItem(b)

        if joy_num > 0:
            self.button_box = self.create_h_box(joy_num)
            self.instruction_layout.addLayout(self.button_box)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
            else:
                self.clearLayout(child)

class SDLInstance:

    # Initialises PySDL2 and the variables to store the joystick data
    def __init__(self):
        self.joystick_control = []
        self.joysticks = []
        self.joystick_axis = []
        self.joystick_ball = []
        self.joystick_hat = []
        self.joystick_button = []

        self.mj = MapJoysticks(self)

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

                # Maps each joystick to a role
                self.mj.update()
                self.mj.show()

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                sdl2.SDL_JoystickClose(self.joysticks[event.jdevice.which])
                self.mj.update()


class ReceiveData(QtGui.QWidget):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, parent=None):
        QtGui.QWidget.__init__(self, parent)  # Initialize PyQt widget
        self.sdl_instance = sdl_instance

    # Runs every cycle and updates the input from the joystick
    def update_input(self):
        self.sdl_instance.update_sdl2()

def getJoysticks():
    if getJoysticks._joysticks is None:
        getJoysticks._joysticks = Joystick()
    return getJoysticks._joysticks
getJoysticks._joysticks = None

class Joystick(QtGui.QWidget):
    def __init__(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
            print "Couldn't initiate joystick(s)."
        else:
            self.sdl_instance = SDLInstance()    # Initializes PySDL2 to read and stores joystick input
            self.joystick_control = self.sdl_instance.joystick_control
            self.joystick_axis = self.sdl_instance.joystick_axis
            self.joystick_ball = self.sdl_instance.joystick_ball
            self.joystick_hat = self.sdl_instance.joystick_hat
            self.joystick_button = self.sdl_instance.joystick_button

            self.rd = ReceiveData(self.sdl_instance)

        self.ready = False

    def start(self):
        # Ties window refresh to joystick refresh
        QtGui.QWidget.__init__(self)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rd.update_input)
        timer.timeout.connect(self.update)
        timer.start(1000 / 120)  # Updates 120 times per second

    def update(self):
        self.joystick_control = self.sdl_instance.joystick_control
        self.joystick_axis = self.sdl_instance.joystick_axis
        self.joystick_ball = self.sdl_instance.joystick_ball
        self.joystick_hat = self.sdl_instance.joystick_hat
        self.joystick_button = self.sdl_instance.joystick_button
        self.ready = True


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)  # app object needs to be declared once per program to make PyQt windows

    js = Joystick()
    js.start()

    window = QtGui.QDialog()
    window.show()
    sys.exit(app.exec_())   # Waits for the 'X' to be clicked to close
