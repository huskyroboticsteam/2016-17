import Parse
from Packet import AuxCtrlID
from PID import PID
from Motor import TalonMC
from Command import Command


class MoveDrill(Command):

    INITIALIZATION_MOTOR_SPEED_MAX = 0.25

    def __init__(self, armatureMotorPin, distanceSensor, limitSwitch, kp=0, ki=0, kd=0):
        # We cannot have undershoot, move slow
        # and calibrate well
        self._pid = PID(kp, ki, kd)
        Command.__init__(self, self._pid)
        self.motor = TalonMC(armatureMotorPin)
        self.distanceSensor = distanceSensor
        self.currentPos = self.distanceSensor.getValue()
        self.limit = limitSwitch
        self.ready = False

    def initialize(self):
        self.motor.enable()
        """
        WILL NOT INITIALIZE WITHOUT LIMIT SWITCH COMMUNICATION CAPABILITY
        """
        while not self.limit.getValue() and self.limit.critical_status:
            self.motor.set(-MoveDrill.INITIALIZATION_MOTOR_SPEED_MAX)
        self.currentPos = self.distanceSensor.getValue()
        self.ready = True

    def run(self, setpoint):
        if setpoint == -1 or not self.ready:
            self.initialize()
        self._pid.setTarget(setpoint)
        self.currentPos = self.distanceSensor.getValue()
        self._pid.run(self.currentPos)
        self.motor.set(self._pid.getOutput())

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.MoveDrill + 1]  # Setpoint distance in mm
        return self._setpoint

    def stopSafe(self):
        self.motor.stop()

    def isFinished(self):
        return False
