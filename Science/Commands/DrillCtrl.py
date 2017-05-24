import Parse
from datetime import datetime
from Motor import TalonMC
from Packet import AuxCtrlID
from PID import PID
from Command import Command


class DrillCtrl(Command):

    def __init__(self,  drillMotorPin):
        Command.__init__(self)
        self.drillMotor = TalonMC(drillMotorPin)

    def initialize(self):
        self.drillMotor.enable()
        self.drillMotor.set(0)

    def run(self, setpoint):
        self.drillMotor.set(self.setpoint() / 100.0)

    def setpoint(self, setpoint=None):
        self._setpoint = Parse.aux_ctrl[AuxCtrlID.DrillRPM + 1]  # Setpoint in RPM
        return self._setpoint

    def stopSafe(self):
        self.drillMotor.stop()

    def isFinished(self):
        return False
