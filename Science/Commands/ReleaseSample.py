import Parse
from Packet import AuxCtrlID
from Motor import Servo
from Commands.Command import Command

class ReleaseSample(Command):
    
    def __init__(self, servo_pin):
        self._motor = Servo(servo_pin)
        Command.__init__(self)

    def initialize(self):
        pass
        #self._motor.moveTo(0.0)

    def run(self, setpoint):
        if setpoint == 1:
            self._motor.moveTo(90.0)
        else:
            self._motor.moveTo(0.0)

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.ReleaseSample + 1]
        return self._setpoint

    def stopSafe(self):
        self._motor.stop()

    def isFinished(self):
        return False
    