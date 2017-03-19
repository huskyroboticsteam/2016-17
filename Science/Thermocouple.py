"""
Reads a Thermocouple amplifier board
(MAX31855)

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
This code has been tested.

"""
import Adafruit_MAX31855.MAX31855 as MAX31855
from Sensor import Sensor
import time
import Util

class Thermocouple(Sensor):

    def __init__(self, clock, cs, data):
        self._device = MAX31855.MAX31855(clock, cs, data)

    def getRawData(self):
        return self._device._read32()

    def getInternalTemp(self):  # degrees C
        time.sleep(0.01)
        return self._device.readInternalC()

    def getTemp(self):
        time.sleep(0.01)
        return self._device.readTempC()

    def getValue(self):
        return self.getTemp(), self.getInternalTemp()

    def getDataForPacket(self):
        raw = self.getRawData() >> 4  # Get rid of status bits
        internalTemp = raw & 0x7FF  # Grab last 11 bits (internal temp reading)
        thermocoupleTemp = raw >> 14  # Grab thermocouple reading
        return Util.inttobin((thermocoupleTemp << 11) & internalTemp, 32)
