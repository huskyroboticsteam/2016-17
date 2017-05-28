import sys
import Parse
import Error
import Util
from Packet import AuxCtrlID
from Commands.Command import Command
from Motor import TalonMC
from PID import PID


class MoveSampleCup(Command):

    LIMITS_ON = True
    INITIALIZATION_MOTOR_SPEED_MAX = 0.15
    MAX_TIME_ALLOTTED_INITIALIZATION = 15

    def __init__(self, motor_pin, limitSwitch, encoder, kp=0, ki=0, kd=0):
        self._motor = TalonMC(motor_pin)
        self._limit = limitSwitch
        self._encoder = encoder
        self.ready = False
        Command.__init__(self, PID(kp, ki, kd))

    def initialize(self):
        # Rotate clockwise until limit is hit (as long as limit plugged in)
        # Reset encoder count
        self._encoder.setAngleK(0.25)  # From Gear reduction on encoder mount
        if MoveSampleCup.LIMITS_ON and not self._limit.getValue():
            self._motor.set(MoveSampleCup.INITIALIZATION_MOTOR_SPEED_MAX)
            self._limit.waitForSwitchChange(MoveSampleCup.MAX_TIME_ALLOTTED_INITIALIZATION)
        self._motor.set(0.0)
        self._encoder.reset()  # Resets to 0 degrees
        self.ready = True

    def run(self, setpoint):
        """
        self._pid.setTarget(setpoint)
        self._pid.run(self._encoder.getAngle())
        self._motor.set(self._pid.getOutput())
        """
        pass

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.MoveSampleCup + 1]
        return self._setpoint

    def stopSafe(self):
        self._motor.stop()

    def isFinished(self):
        return False

