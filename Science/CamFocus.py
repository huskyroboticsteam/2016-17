import Parse
from Packet import AuxCtrlID
from Command import Command
from PID import PID


class CamFocus(Command):

    def __init__(self, servoSigPin, kp=0, ki=0, kd=0):
        self._pid = PID(kp, ki, kd)
        Command.__init__(self, self._pid)
        self._pin = servoSigPin

    def initialize(self):
        pass  # Initialize the servo etc.

    def run(self, setpoint):
        self._pid.setTarget(setpoint)
        self._pid.run(0)  # Current Servo Pos Here

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.CamFocusPos + 1]
        return self._setpoint

    def stopSafe(self):
        pass  # Stop Moving Servo Here

    def isFinished(self):
        return False  # Tells when to finish command
