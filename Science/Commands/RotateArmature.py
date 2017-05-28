import time
import Util
from math import fabs
from Command import Command
from PID import PID
from Motor import TalonMC
from math import pi

class RotateArmature(Command):

    LIMITS_ON = True

    INITIALIZATION_MOTOR_SPEED_MAX = 0.5  # %/100 MAX VALUE
    MAX_TIME_ALLOTTED_INITIALIZATION = 15   # SECONDS

    def __init__(self, armatureMotorPin, encoder, limitSwitch, kp=0, ki=0, kd=0):
        Command.__init__(self, PID(kp, ki, kd))
        self._motor = TalonMC(armatureMotorPin)
        self._encoder = encoder
        self._limit = limitSwitch
        self.ready = False

    def initialize(self):
        self._encoder.setAngleK(0.25)  # From Gear reduction on encoder mount
        if RotateArmature.LIMITS_ON and not self._limit.getValue():
            self._motor.set(RotateArmature.INITIALIZATION_MOTOR_SPEED_MAX)
            self._limit.waitForSwitchChange(RotateArmature.MAX_TIME_ALLOTTED_INITIALIZATION)
        self._motor.set(0)
        self._encoder.reset()  # Resets to 0 degrees
        self.ready = True

    def run(self, setpoint):
        pass

    def stopSafe(self):
        self._motor.stop()


