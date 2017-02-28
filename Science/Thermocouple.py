"""
Reads a Thermocouple amplifier board
(MAX31855)

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
This code has been tested.

"""
import Adafruit_MAX31855.MAX31855 as MAX31855


class Thermocouple:

    def __init__(self, clock, cs, data):
        self._device = MAX31855.MAX31855(clock, cs, data)

    def getData(self):
        return self._device._read32()

    def getInternalTemp(self):  # degrees C
        return self._device.readInternalC()

    def getTemp(self):
        return self._device.readTempC()