import sys
import Parse
import Error
import Util
from Packet import AuxCtrlID
from Command import Command
from Motor import Servo


class CamFocus(Command):

    def __init__(self, servo_pin):
        self._motor = Servo(servo_pin)
        Command.__init__(self)

    def initialize(self):
        pass

    def run(self, setpoint):
        self._motor.moveTo(setpoint)

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.CamFocusPos + 1]
        return self._setpoint

    def stopSafe(self):
        self._motor.stop()

    def isFinished(self):
        return False
