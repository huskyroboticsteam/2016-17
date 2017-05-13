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

    def init_joy_vars(self, joy_num):
        self.joystick_axis = []
        self.joystick_ball = []
        self.joystick_hat = []
        self.joystick_button = []

        for i in range(joy_num):
            self.joysticks.append(sdl2.SDL_JoystickOpen(i))
            axis_num = sdl2.SDL_JoystickNumAxes(self.joysticks[i])
            ball_num = sdl2.SDL_JoystickNumBalls(self.joysticks[i])
            hat_num = sdl2.SDL_JoystickNumHats(self.joysticks[i])
            button_num = sdl2.SDL_JoystickNumButtons(self.joysticks[i])

            self.joystick_axis.append([])
            for j in range(axis_num):
                self.joystick_axis[i].append(0)     # [axis1, axis2, axis2, ...]

            self.joystick_ball.append([])
            for j in range(ball_num):
                self.joystick_ball[i].append([0, 0])   # [[x, y]]

            for j in range(hat_num):
                self.joystick_hat.append(0)  # [[direction]]

            self.joystick_button.append([])
            for j in range(button_num):
                self.joystick_button[i].append(0)  # [button1, button2, button3, ...]

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
                pass

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                # Disconnect isn't working
                pass


class ReceiveData(QtGui.QWidget):
    # Creates a window of for joystick
    def __init__(self, sdl_instance, parent=None):
        QtGui.QWidget.__init__(self, parent)  # Initialize PyQt widget
        self.sdl_instance = sdl_instance

    # Runs every cycle and updates the input from the joystick
    def update_input(self):
        self.sdl_instance.update_sdl2()
        
# Singleton
def getJoysticks():
    if getJoysticks._joysticks is None:
        getJoysticks._joysticks = Joysticks()
    return getJoysticks._joysticks
getJoysticks._joysticks = None
        
class Joysticks(QtGui.QWidget):
    
    def __init__(self):
        """
        Don't call this directly, instead use getJoysticks()
        """
        if sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK) < 0:
            print "Couldn't initiate joystick(s)."
        else:
            self.sdl_instance = SDLInstance()    # Initializes PySDL2 to read and stores joystick input

            joy_num = sdl2.SDL_NumJoysticks()
            self.sdl_instance.init_joy_vars(joy_num)

            self.rd = ReceiveData(self.sdl_instance)

            self.joystick_axis = []
            self.joystick_ball = []
            self.joystick_button = []
            self.joystick_hat = []
        self.ready = False

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
        
        # Enable to debug the raw input from the joystick
        #print str(self.joystick_axis[0])+ " " + str(self.joystick_button[0]) + " " + str(self.joystick_hat[0])
        
        self.ready = True
