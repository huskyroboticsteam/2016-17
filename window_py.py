import sdl2
import sdl2.ext
from PyQt4 import QtCore, QtGui

# Handles input
class SDLInstance:
    max_axis_value = 2**15

    # Initialises PySDL and the variables to store the joystick data
    def __init__(self):
        # Setup SDL2
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
        self.joystick = sdl2.SDL_JoystickOpen(0)

        # Variables to store joystick input
        self.whichJoystick = None
        self.joystick_axis = [0, 0, 0, 0]

        self.whichJoystickBall = None
        self.joystickBall = None
        self.joystickBallXRel = None
        self.joystickBallYRel = None

        self.whichjoystickHat = None
        self.joystickHat = None
        self.joystickHatValue = None

        self.whichJoystickButtonUp = None
        self.joystickButtonUp = None
        self.joystickButtonStateUp = None

        self.whichJoystickButtonDown = None
        self.joystickButtonDown = None
        self.joystickButtonStateDown = None

        self.joystickAdded = None
        self.joystickRemoved = None

        self.joystickConnected = False

    # The following 7 functions allow for the info to be accessed outside of the class
    def getAxisData(self):
        return self.whichJoystick, self.joystick_axis

    def getBallData(self):
        return self.whichJoystickBall, self.joystickBall, self.joystickBallXRel, self.joystickBallYRel

    def getHatData(self):
        return self.whichjoystickHat, self.joystickHat, self.joystickHatValue

    def getButtonUpData(self):
        return self.whichJoystickButtonUp, self.joystickButtonUp, self.joystickButtonStateUp

    def getButtonDownData(self):
        return self.whichJoystickButtonDown, self.joystickButtonDown, self.joystickButtonStateDown

    def getJoystickAddedData(self):
        return self.joystickAdded

    def getJoystickRemovedData(self):
        return self.joystickRemoved

    def getJoystickConnected(self):
        return self.joystickConnected

    # Takes the joystick input and stores in variables to be accessed later
    def update_sdl2(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.whichJoystick = event.jaxis.which
                self.joystick_axis[event.jaxis.axis] = event.jaxis.value

            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.whichJoystickBall = event.jball.which
                self.joystickBall = event.jball.ball
                self.joystickBallXRel = event.jball.xrel
                self.joystickBallYRel = event.jball.yrel

            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.whichjoystickHat = event.jhat.which
                self.joystickHat = event.jhat.hat
                self.joystickHatValue = event.jhat.value

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                self.whichJoystickButtonUp = event.jbutton.which
                self.joystickButtonUp = event.jbutton.button
                self.joystickButtonStateUp = event.jbutton.state

            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.whichJoystickButtonDown = event.jbutton.which
                self.joystickButtonDown = event.jbutton.button
                self.joystickButtonStateDown = event.jbutton.state

            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.joystickAdded = event.jdevice.which
                sdl2.SDL_JoystickOpen(0)
                self.joystickConnected = True

            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.joystickRemoved = event.jdevice.which
                self.joystickConnected = False

class MainApplication(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self)    # Initialize PyQt widget
        self.timer = QtCore.QTimer(self)
        for i in args:
            self.timer.timeout.connect(i)   # Runs this function every refresh

    def start_timer(self):
        self.timer.start(1000 / 120)    # 1000 milliseconds divided by 120, updates 120 times per second

class DisplayInputData(QtGui.QWidget):
    # Initializes the widget
    def __init__(self, sdl_instance, parent=None):
        # Setup PyQt
        QtGui.QWidget.__init__(self, parent)    # Initialize PyQt widget
        self.setGeometry(300, 300, 200, 200)    # Set window dimensions (x, y, w, h)
        self.setWindowTitle("Joystick Data")  # Sets the title of the window
        self.layout = QtGui.QVBoxLayout(self)  # Layout to use for each label of the window
        self.pyqtWindow()  # Initializes labels for the window
        # Sets the background color to white
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)
        self.sdlInst = sdl_instance

    def update_l2(self):
        self.sdlInst.update_sdl2()   # Checks for new input

        joystickData = ""

        if self.sdlInst.getJoystickConnected() == True:
            # String containing the input data to be displayed on the window, broken up for "readability"
            joystickData = "Joystick: " + str(self.sdlInst.getAxisData()[0]) + "\nValues: " + str(
                self.sdlInst.getAxisData()[1]) + "\n\n"
            joystickData += "Ball on Joystick: " + str(self.sdlInst.getBallData()[0]) + "\nValue: " + str(
                self.sdlInst.getBallData()[1]) + "\nxrel: " + str(self.sdlInst.getBallData()[2]) + "\nyrel" + str(
                self.sdlInst.getBallData()[3]) + "\n\n"
            joystickData += "Hat on Joystick: " + str(self.sdlInst.getHatData()[0]) + "\nHat: " + str(
                self.sdlInst.getHatData()[1]) + "\nValue: " + str(self.sdlInst.getHatData()[2]) + "\n\n"
            joystickData += "Button Up on Joystick: " + str(self.sdlInst.getButtonUpData()[0]) + "\nButton: " + str(
                self.sdlInst.getButtonUpData()[1]) + "\nState: " + str(self.sdlInst.getButtonUpData()[2]) + "\n\n"
            joystickData += "Button Down on Joystick: " + str(self.sdlInst.getButtonDownData()[0]) + "\nButton: " + str(
                self.sdlInst.getButtonDownData()[1]) + "\nState: " + str(self.sdlInst.getButtonDownData()[2]) + "\n\n"
            joystickData += "Joystick Added: " + str(self.sdlInst.getJoystickAddedData()) + "\n"
            joystickData += "Joystick Removed: " + str(self.sdlInst.getJoystickRemovedData()) + "\n"
        elif self.sdlInst.getJoystickConnected() == False:
            self.resize(200, 100)
            joystickData = "Joystick Not Connected"

        self.l2.setText(joystickData)  # Sets label "l2" to the String joystickData

    def pyqtWindow(self):
        self.l2 = QtGui.QLabel()  # Creates label object for the joystick output
        self.l2.setAlignment(QtCore.Qt.AlignCenter)  # Aligns the label to the center
        self.layout.addWidget(self.l2)  # Adds the label widget to the layout

# Displays a representation of the joysticks (a white square) position
class JoystickPosition(QtGui.QWidget):
    # Initializes the widget
    def __init__(self, sdl_instance, parent=None):
        QtGui.QWidget.__init__(self, parent)    # Initialize PyQt widget
        self.windowWidth, self.windowLength = 200, 200
        self.setGeometry(600, 300, self.windowWidth, self.windowLength)     # Set window dimensions (x, y, w, h)
        self.setWindowTitle("Joystick Position")    # Sets the title of the window
        self.layout = QtGui.QVBoxLayout(self)  # Layout to use for each label of the window
        # Sets the background color to black
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)
        self.sdl_instance = sdl_instance

    def paintEvent(self, event):
        # White square
        qp = QtGui.QPainter()
        qp.begin(self)  # Allows for objects to be "painted" on the window
        qp.setBrush(QtGui.QColor(255, 255, 255))    # Sets the square color (r, g, b)
        squareWidth, squareLength = 10, 10
        horiz_axis, vert_axis, twist, flap = self.sdl_instance.joystick_axis
        self.x = self.windowWidth / 2 - squareWidth / 2 + (float(horiz_axis) / self.sdl_instance.max_axis_value)*(self.windowWidth/2)
        self.y = self.windowLength / 2 - squareLength / 2 + (float(vert_axis) / self.sdl_instance.max_axis_value)*(self.windowLength/2)
        qp.drawRect(self.x, self.y, squareWidth, squareLength)  # Centers the white square (representing an idle joystick) (x, y, w, h)
        qp.end()    # Restricts further objects from being "painted" on the window
    '''
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Up:
            self.y = 0
            print "Up"
        if QKeyEvent.key() == QtCore.Qt.Key_Down:
            print "Down"
    '''

# Displays a representation of the rover's (a red square) position
class RoverPosition(QtGui.QWidget):
    # Initializes the widget
    def __init__(self, sdl_instance, parent=None):
        QtGui.QWidget.__init__(self, parent)    # Initialize PyQt widget
        self.windowWidth, self.windowLength = 300, 300
        self.setGeometry(900, 300, self.windowWidth, self.windowLength)     # Set window dimensions (x, y, w, h)
        self.setWindowTitle("Rover Position")   # Sets the title of the window
        self.layout = QtGui.QVBoxLayout(self)  # Layout to use for each label of the window
        # Sets the background color to white
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.white)
        self.setPalette(p)
        self.sdl_instance = sdl_instance

    # Draws the rover (a red square)
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)  # Allows for objects to be "painted" on the window
        # Red square
        qp.setBrush(QtGui.QColor(255, 0, 0))    # Sets the rover color (r, g, b)
        self.squareX, self.squareY, squareWidth, squareLength = 0, 0, 25, 25
        qp.drawRect(self.squareX, self.squareY, squareWidth, squareLength)      # Sets the rovers initial position (x, y, w, h)
        qp.end()    # Restricts further objects from being "painted" on the window