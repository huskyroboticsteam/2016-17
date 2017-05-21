import Parse
from Packet import AuxCtrlID
from PID import PID
from Motor import TalonMC
from Command import Command


class MoveDrill(Command):

    def __init__(self, armatureMotorPin, distanceSensor, kp=0, ki=0, kd=0):
        # We cannot have undershoot, move slow
        # and calibrate well
        self._pid = PID(kp, ki, kd)
        Command.__init__(self, self._pid)
        self.motor = TalonMC(armatureMotorPin)
        self.distanceSensor = distanceSensor
        self.currentPos = self.distanceSensor.getValue()

    def initialize(self):
        self.motor.enable()
        self.currentPos = self.distanceSensor.getValue()

    def run(self, setpoint):
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
