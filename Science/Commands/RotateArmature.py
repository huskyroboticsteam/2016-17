from Command import Command
from Motor import TalonMC


class RotateArmature(Command):

    def __init__(self, armatureMotorPin, encoder):
        Command.__init__(self)
        self._motor = TalonMC(armatureMotorPin)
        self._encoder = encoder

    def initialize(self):
        pass

    def run(self, reading):
        pass

    def stopSafe(self):
        self._motor.stop()


