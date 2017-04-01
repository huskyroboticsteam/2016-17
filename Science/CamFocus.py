from Command import Command
from PID import PID


class CamFocus(Command):

    def __init__(self):
        self._pid = PID(0, 0, 0)
        Command.__init__(self, self._pid)

    def initialize(self):
        pass  # Initialize the servo etc.

    def run(self, setpoint):
        self._pid.setTarget(setpoint)
        self._pid.run(0)  # Current Servo Pos Here

    def stopSafe(self):
        pass  # Stop Moving Servo Here

    def isFinished(self):
        return False  # Tells when to finish command
