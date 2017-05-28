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
    INITIALIZATION_MOTOR_SPEED_MAX = 0.05

    def __init__(self, motor_pin, limitSwitch, encoder, kp=0, ki=0, kd=0):
        self._motor = TalonMC(motor_pin)
        self._limit = limitSwitch
        self._encoder = encoder
        self.ready = False
        Command.__init__(self, PID(kp, ki, kd))

    def initialize(self):
        # Rotate clockwise until limit is hit (as long as limit plugged in)
        # Reset encoder count
        limitFound = False
        """
        while not limitFound and not self._limit.critical_status and MoveSampleCup.LIMITS_ON:
            if self._limit.getValue():
                limitFound = True
            self._motor.set(-MoveSampleCup.INITIALIZATION_MOTOR_SPEED_MAX)
        if limitFound:
            self._encoder.reset()
        self.ready = True
        """

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

