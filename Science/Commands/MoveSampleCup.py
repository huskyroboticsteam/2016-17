import sys
import Parse
import Error
import Util
import time
from Packet import AuxCtrlID
from Commands.Command import Command
from Motor import TalonMC
from PID import PID


class MoveSampleCup(Command):

    LIMITS_ON = True
    INITIALIZATION_MOTOR_SPEED_MAX = 0.15
    RUNTIME_MAX_SPEED = 0.2
    MAX_TIME_ALLOTTED_INITIALIZATION = 15

    def __init__(self, motor_pin, limitSwitch, encoder, kp=0, ki=0, kd=0):
        self._motor = TalonMC(motor_pin)
        self._limit = limitSwitch
        self._encoder = encoder
        self.ready = False
        self.last_setpoint = 0.0
        self.last_pid_output = 0.0
        Command.__init__(self, PID(kp, ki, kd))

    def initialize(self):
        # Rotate clockwise until limit is hit (as long as limit plugged in)
        # Reset encoder count
        self._encoder.setAngleK(1.1)  # Calibrated as good as possible
        self._encoder.setReverse()  # Reverses positive / negative direction of encoder angle/distance
        if MoveSampleCup.LIMITS_ON and not self._limit.getValue():
            self._motor.set(MoveSampleCup.INITIALIZATION_MOTOR_SPEED_MAX)
            self._limit.waitForSwitchChange(MoveSampleCup.MAX_TIME_ALLOTTED_INITIALIZATION)
        self._motor.set(0.0)
        self._encoder.reset()  # Resets to 0 degrees
        self.ready = True
        self._pid.restrainedOutput(MoveSampleCup.RUNTIME_MAX_SPEED)  # Restrains output

    def run(self, setpoint):
        if self._encoder.getAngleDegrees() > 360.0:
            self.initialize()
        self._pid.setTarget(setpoint)
        self._pid.run(self._encoder.getAngleDegrees())
        output = self._pid.getOutput()
        if output != self.last_pid_output:
            pass
            #Util.write(output)
        self._motor.set(output)
        self.last_pid_output = output

    def setpoint(self, setpoint=None):
        # Retrieves setpoint from packet
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.MoveSampleCup + 1]
        self.last_setpoint = self._setpoint
        return self._setpoint

    def stopSafe(self):
        self._motor.stop()

    def isFinished(self):
        return False

