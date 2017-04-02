"""
Communicates with VL53L0X Time-of-Flight Distance Sensor
on the Beaglebone Black

Written by Jaden Bottemiller in February 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Tested as of 2/26/2017)

VL53L0X Documentation:
https://www.pololu.com/file/download/VL53L0X.pdf?file_id=0J1187


NOTE: You will need the library found here: https://github.com/johnbryanmoore/VL53L0X_rasp_python
      and follow this issue thread here step by step https://github.com/johnbryanmoore/VL53L0X_rasp_python/issues/1
      to get it to work on the Beaglebone Black.
      * For the purposes of the 2016-17 build season, you can copy the VL53L0X_rasp_python folder and the VL53L0X.py
        file in this directory to skip this step. THE FOLDER IN THIS DIRECTORY HAS EDITED FILES FROM THE ORIGINAL

NOTE: There are more options for the operation of the ToF Sensor than the operations that this object allows.
      Look through the supplied class in the VL53L0X library for full functionality. These are very basic
      operations.

NOTE: getDistance() takes an average of 30ms according to the documentation, so if
      your code is more time sensitive, it may make more sense to create a thread and
      run this code in the background.
      A good tutorial on threads: https://www.youtube.com/watch?v=EvbA3qVMGaw

NOTE: If you do not call startRanging() BEFORE getDistance(), it will take at least 10x as long to receive the result.

NOTE: It is recommended to call stopRanging() at the end of getting distances, but not required. See VL53L0X
      documentation for more details on ranging.

"""

import VL53L0X
import time


class DistanceSensor:

    _ranging = False
    _distance = 0

    def __init__(self):
        self._sensor = None
        self._sensor = VL53L0X.VL53L0X()

    def start(self):
        self._sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        self._ranging = True

    def stop(self):
        if not self.critical_status:
            self._sensor.stop_ranging()
            self._ranging = False

    def getValue(self):
        if not self._ranging:
            self.start()
        time.sleep(0.3)
        timing = self._sensor.get_timing()
        if timing < 20000:
            timing = 20000
        self._distance = self._sensor.get_distance()
        time.sleep(timing / 1000000.00)
        return self._distance
