from PID import PID
from Command import Command


class MoveDrill(Command):

    def __init__(self):
        # We cannot have undershoot, move slow
        # and calibrate well
        self._pid = PID(0, 0, 0)
        Command.__init__(self, self._pid)

    def initialize(self):
        pass

    def run(self, setpoint):
        self._pid.setTarget(setpoint)
        self._pid.run(0)  # Current drill pos above ground (mm)

    def stopSafe(self):
        pass

    def isFinished(self):
        return False
