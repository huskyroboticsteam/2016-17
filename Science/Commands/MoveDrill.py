import Parse
import time
import Util
from Packet import AuxCtrlID
from PID import PID
from Motor import TalonMC
from Command import Command


class MoveDrill(Command):

    INITIALIZATION_MOTOR_SPEED_MAX = 0.2
    MAX_TIME_ALLOTTED_INITIALIZATION = 10
    LIMITS_ON = True

    def __init__(self, armatureMotorPin, distanceSensor, encoder, limitSwitch, kp=0, ki=0, kd=0):
        # We cannot have undershoot, move slow
        # and calibrate well
        self._pid = PID(kp, ki, kd)
        Command.__init__(self, self._pid)
        self._motor = TalonMC(armatureMotorPin)
        self._distanceSensor = distanceSensor
        self._encoder = encoder
        self._limit = limitSwitch
        self.last_setpoint = 0.0
        self.ready = False

    def initialize(self):
        self._encoder.setDistanceK(0.011)  # From radius of encoder wheel in meters
        if MoveDrill.LIMITS_ON and not self._limit.getValue():
            self._motor.set(-MoveDrill.INITIALIZATION_MOTOR_SPEED_MAX)
            self._limit.waitForSwitchChange(MoveDrill.MAX_TIME_ALLOTTED_INITIALIZATION)
        self._motor.set(0)
        self.ready = True
        self._encoder.reset()
        self._motor.set(0.15)
        time.sleep(4)
        self._motor.set(0)

    def run(self, setpoint):
        self.last_setpoint = setpoint
        if setpoint == -1 or not self.ready:
            self.initialize()
        self._pid.setTarget(setpoint)
        self.currentPos = self._encoder.getDistance()
        self._pid.run(self.currentPos)
        output = self._pid.getOutput()
        if self._limit.getValue() and output < 0:
            self._motor.set(0.0)  # For safety
        else:
            self._motor.set(output)

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.MoveDrill + 1]  # Setpoint distance in mm
        return self._setpoint / 1000.0

    def stopSafe(self):
        self.motor.stop()

    def isFinished(self):
        return False
