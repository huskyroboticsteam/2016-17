import Parse
from datetime import datetime
from Motor import TalonMC
from Packet import AuxCtrlID
from PID import PID
from Command import Command


class DrillCtrl(Command):

    def __init__(self,  drillMotorPin, drillEncoder, kp=0, ki=0, kd=0):
        self._pid = PID(kp, ki, kd)
        Command.__init__(self, self._pid)
        self.drillMotor = TalonMC(drillMotorPin)
        self.drillEncoder = drillEncoder
        self.currentPos = 0
        self.currentRate = 0
        self.lastTime = datetime.now().microsecond

    def initialize(self):
        self.drillMotor.enable()
        self.currentPos = self.drillEncoder.getValue()[0]
        self.currentRate = 0

    def run(self, setpoint):
        # Set setpoint of PID controller to given setpoint
        self._pid.setTarget(setpoint)

        # Find current rate
        now = datetime.now().microsecond
        deltaT = now - self.lastTime
        self.lastTime = now
        currentP = self.drillEncoder.getValue()[0]
        self.currentRate = (currentP - self.currentPos) / deltaT
        self.currentRate = 21600.0 / self.currentRate  # Convert from */s to RPM
        self.currentPos = currentP

        # Run PID Controller
        self._pid.run(self.currentRate)
        # Set motor to new speed
        self.drillMotor.set(self._pid.getOutput())

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.DrillRPM + 1]  # Setpoint in RPM
        return self._setpoint

    def stopSafe(self):
        self.drillMotor.stop()

    def isFinished(self):
        return False
