"""
Very early development on this communication...
"""

import VL53L0X
import time


class DistanceSensor:

    _ranging = False

    def __init__(self):
        self._sensor = VL53L0X.VL53L0X()

    def startRanging(self):
        self._sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self._ranging = True

    def stopRanging(self):
        self._sensor.stop_ranging()
        self._ranging = False

    def getDistance(self):
        if not self._ranging:
            self.startRanging()
            time.sleep(0.3)
        timing = self._sensor.get_timing()
        if timing < 20000:
            timing = 20000
        distance = self._sensor.get_distance()
        time.sleep(timing / 1000000.00)
        return distance
