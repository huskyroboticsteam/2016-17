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

    def __repr__(self):
        return "<index: {}, axis: {}, ball: {}, hat: {}, button: {}>".format(
            self.id,
            self.axis,
            self.ball,
            self.hat,
            self.button
        )

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


class _JoystickManager:
    """Manages joystick instances"""

    def __init__(self):
        self.joysticks = dict()
        self._sdl_update_loop = None
        self._callbacks = list()

        for index in range(sdl2.SDL_NumJoysticks()):
            self.joysticks[index] = _Joystick(index)

    def start(self):
        """
        Starts the joystick listening loop.
        
        Run this after the Qt application has already started
        """
        self._sdl_update_loop = _SDLUpdateLoop()
        self._sdl_update_loop.start_loop(self._sdl2_update_loop)

    def add_callback(self, callback):
        """Adds a callback after a SDL2 update event is processed"""
        self._callbacks.append(callback)

    def _sdl2_update_loop(self):
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                self.joysticks[event.jaxis.which].axis[event.jaxis.axis] = event.jaxis.value
            elif event.type == sdl2.SDL_JOYBALLMOTION:
                self.joysticks[event.jball.which].ball[event.jball.ball] = (event.jball.xrel, event.jball.yrel)
            elif event.type == sdl2.SDL_JOYHATMOTION:
                self.joysticks[event.jhat.which].hat[event.jhat.hat] = event.jhat.value
            elif event.type == sdl2.SDL_JOYBUTTONUP or event.type == sdl2.SDL_JOYBUTTONDOWN:
                self.joysticks[event.jbutton.which].button[event.jbutton.button] = event.jbutton.state
            elif event.type == sdl2.SDL_JOYDEVICEADDED:
                self.joysticks[event.jdevice.which] = _Joystick(event.jdevice.which)
            elif event.type == sdl2.SDL_JOYDEVICEREMOVED:
                self.joysticks[event.jdevice.which].close()
                del self.joysticks[event.jdevice.which]
        for callback in self._callbacks:
            callback()

joystick_manager = _JoystickManager()

if __name__ == "__main__":
    # Code that runs when the script is invoked directly
    def _main():
        import sys
        app = QtGui.QApplication(sys.argv)
        def print_callback():
            print(joystick_manager.joysticks)
        joystick_manager.add_callback(print_callback)
        joystick_manager.start()
        window = QtGui.QDialog()
        window.show()
        sys.exit(app.exec_())
    _main()
