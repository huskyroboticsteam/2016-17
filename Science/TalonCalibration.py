import time


class TalonCalibration:

    def __init__(self, motor):
        self._motor = motor

    def calibrate(self):
        start_time = time.time()
        while time.time() - start_time < 5:
            self._motor.set(1.0)
        start_time = time.time()
        while time.time() - start_time < 5:
            self._motor.set(0.0)
