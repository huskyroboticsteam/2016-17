import Adafruit_MAX31855.MAX31855 as MAX31855


class Thermocouple(object):

    def __init__(self, clock, cs, data):
        self._device = MAX31855.MAX31855(clock, cs, data)

    def getData(self):
        return self._device._read32()

    def getInternalTemp(self): # degrees C
        return self._device.readInternalC()

    def getTemp(self):
        return self._device.readTempC()