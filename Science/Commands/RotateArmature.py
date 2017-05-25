import time
from Command import Command
from PID import PID
from Motor import TalonMC
from math import pi

class RotateArmature(Command):

    LIMITS_ON = True

    INITIALIZATION_MOTOR_SPEED_MAX = 0.25  # % MAX VALUE
    ALLOWABLE_INITIALIZATION_TOLERANCE = pi/16  # RADIANS
    MAX_TIME_ALLOTTED_INITIALIZATION = 30  # SECONDS
    INITIALIZATION_kP = 0.01
    INITIALIZATION_kI = 0.01
    INITIALIZATION_kD = 0.01

    def __init__(self, armatureMotorPin, encoder, limitSwitch, kp=0, ki=0, kd=0):
        Command.__init__(self, PID(kp, ki, kd))
        self._motor = TalonMC(armatureMotorPin)
        self._encoder = encoder
        self._limit = limitSwitch
        self.ready = False

    def initialize(self):
        self.encoder.setAngleK(0.25)  # From Gear reduction on encoder mount
        # Move 30* Left or until limit switch found; then,
        # Move 60* Right or until limit switch found
        limitFound = False
        initEncoderAngle = self._encoder.getAngle()
        firstTarget = initEncoderAngle - (pi/6)
        secondTarget = initEncoderAngle + (pi/6)
        self._pid.setTarget(firstTarget)
        self._pid.setCoefficients(RotateArmature.INITIALIZATION_kP, RotateArmature.INITIALIZATION_kI, RotateArmature.INITIALIZATION_kP)
        startTime = time.time()
        """
        WILL NOT FIND ANGLE INITIALIZATION WITHOUT LIMIT SWITCH COMMUNICATION CAPABILITY
        """
        while not limitFound and not self._limit.critical_status and RotateArmature.LIMITS_ON:
            if self._limit.getValue():
                limitFound = True
            if self._pid.getError <= RotateArmature.ALLOWABLE_INITIALIZATION_TOLERANCE:
                self._pid.setTarget(secondTarget)
            if time.time() - startTime > RotateArmature.MAX_TIME_ALLOTTED_INITIALIZATION:
                # TODO: Throw armature roation initialization timed out
                break
            self._pid.run(self._encoder.getAngle())
            self._motor.set(self._pid.restrainedOutput(RotateArmature.INITIALIZATION_MOTOR_SPEED_MAX))
        if limitFound:
            self._encoder.reset()
        self._pid.setCoefficients(self.kp, self.ki, self.kd)  # Reset PID coefficients to original values
        self.ready = True

    def run(self, setpoint):
        pass

    def stopSafe(self):
        self._motor.stop()


