"""
This class is meant to be used to calibrate a Talon
Motor Controller.

Documentation on calibration here:
https://content.vexrobotics.com/vexpro/pdf/Talon-SRX-Users-Guide-20170226.pdf
Page 29 has PWM Calibration information

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Tested as of 2/25/2017)


"""

import time


class TalonCalibration:

    def __init__(self, motor):
        self._motor = motor

    def calibrate(self):
        start_time = time.time()
        while time.time() - start_time < 0.5:
            self._motor.set(1.0)
        start_time = time.time()
        while time.time() - start_time < 0.5:
            self._motor.set(0.0)
