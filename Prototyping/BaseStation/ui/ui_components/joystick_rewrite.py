from PyQt4 import QtCore, QtGui

import sdl2
import sdl2.ext

"""
Joystick interface implemented with PySDL2

Should only be used only with other PyQt code so Qt's internal event loop will prevent
any race conditions.
"""

sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)


class _Joystick:
    """Instance of a joystick"""

    def __init__(self, index):
        """Initializes a Joystick object and opens the SDL2 joystick"""

        self.id = index

        self._sdl_joystick_obj = sdl2.SDL_JoystickOpen(index)

        self.axis_count = sdl2.SDL_JoystickNumAxes(self._sdl_joystick_obj)
        self.ball_count = sdl2.SDL_JoystickNumBalls(self._sdl_joystick_obj)
        self.hat_count = sdl2.SDL_JoystickNumHats(self._sdl_joystick_obj)
        self.button_count = sdl2.SDL_JoystickNumButtons(self._sdl_joystick_obj)

        self.axis = list()
        for i in range(self.axis_count):
            self.axis.append(0)

        self.ball = list()
        for i in range(self.ball_count):
            self.ball.append(0)

        self.hat = list()
        for i in range(self.hat_count):
            self.hat.append(0)

        self.button = list()
        for i in range(self.button_count):
            self.button.append(0)

    def close(self):
        """Closes the joystick in SDL2"""
        sdl2.SDL_JoystickClose(self._sdl_joystick_obj)


class _SDLUpdateLoop(QtGui.QWidget):
    """Continuously invokes a method via a QTimer"""

    def start_loop(self, *args):
        """Starts the loop with the callback methods given"""
        self._timer = QtCore.QTimer()
        for callback in args:
            self._timer.timeout.connect(callback)
        self._timer.start(1000 / 120) # Update at 120 Hz


class JoystickManager:
    """Manages joystick instances"""

    def __init__(self):
        self.joysticks = dict()
        self._sdl_update_loop = _SDLUpdateLoop()
        self._sdl_update_loop.start_loop(self._sdl2_update_loop)

        for index in range(sdl2.SDL_NumJoysticks()):
            self.joysticks[index] = _Joystick(index)

    def _sdl2_update_loop(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.joysticks[event.which].axis[event.axis] = event.value
            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.joysticks[event.which].ball[event.ball] = (event.xrel, event.yrel)
            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.joysticks[event.which].hat[event.hat] = event.value
            elif event.type == sdl2.SDL_JOYBUTTONUP or event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.joysticks[event.which].button[event.button] = event.state
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.joysticks[event.which] = _Joystick(event.which)
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.joysticks[event.which].close()
                del self.joysticks[event.which]
