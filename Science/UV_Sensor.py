"""
Reads a UV Sensor board through I2C

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
This code has been tested.
"""

import Adafruit_GPIO.I2C as I2C


class UV:

    # default time constant
    _uvTConst = 0x02

    # initialize device with the correct LSB address given in the
    # documentation.
    def __init__(self, LSB_ADDR):
        self._uvl = I2C.Device(LSB_ADDR, I2C.get_default_bus())
        self._uvm = I2C.Device(LSB_ADDR + 1, I2C.get_default_bus())
        self.setup(self._uvTConst)

    # Sets up device with time constant
    def setup(self, tConst):  # tConst = 0, 1, 2, 3
        _uvTConst = tConst & 3  # Removes any unwanted digits
        self._uvl.writeRaw8((_uvTConst << 2) | 2)  # Writes to correct register

    # Reads raw binary value from the register
    def getRaw(self):
        uvData = self._uvl.readRaw8()
        uvData |= self._uvm.readRaw8() << 8
        return uvData

    # Gets data in uW/cm/cm
    def getData(self):
        return self.getRaw() * 5  # uW/cm/cm (multiplication factor of 5 given by the datasheet)
