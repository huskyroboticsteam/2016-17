import Parse
import Error
from Packet import AuxCtrlID
from Command import Command
from Motor import Servo

DEFAULT_PIN = "P8_45"


class CamFocus(Command):

    def __init__(self, servo_pin=DEFAULT_PIN):
        Command.__init__(self, self._pid)
        self._motor = Servo(servo_pin)

    def initialize(self):
        pass  # Initialize the servo, sets everything to relaxed state

    def run(self, setpoint):
        self._motor.moveTo(setpoint)

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.CamFocusPos + 1]
        return self._setpoint

    def stopSafe(self):
        self._motor.stop()

    def isFinished(self):
        return False  # Tells when to finish command
