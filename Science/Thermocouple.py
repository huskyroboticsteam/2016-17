"""
Reads a Thermocouple amplifier board
(MAX31855)

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
This code has been tested.

"""
import Error
import time
import Util
import Adafruit_MAX31855.MAX31855 as MAX31855
from Sensor import Sensor


class Thermocouple(Sensor):

    def __init__(self, clock, cs, data):
        self._device = None
        self.critical_status = False
        try:
            self._device = MAX31855.MAX31855(clock, cs, data)
        except:
            # Throw "Communication Failure"
            Error.throw(0x0108, "Could not initialize thermocouple communications")
            self.critical_status = True
        self.critical_status = self.checkError()

    def getRawData(self):
        if self.critical_status:
            return 0
        raw = 0
        try:
            raw = self._device._read32()
        except:
            # Throw "Communication Failure"
            Error.throw(0x0108)
        return raw

    def getInternalTemp(self):  # degrees C
        self.checkError()
        if self.critical_status:
            return 0
        self.checkError()
        time.sleep(0.01)
        internal_temp = 0
        try:
            internal_temp = self._device.readInternalC()
        except:
            # Throw "Could not get internal reading"
            Error.throw(0x0102)
        if not Util.isValidUnsigned(internal_temp):
            # Throw "Reading Invalid"
            Error.throw(0x0103)
        return internal_temp

    def getTemp(self):
        self.checkError()
        if self.critical_status:
            return 0
        time.sleep(0.01)
        temp = 0
        try:
            temp = self._device.readTempC()
        except:
            # Throw "Could not get reading"
            Error.throw(0x0101)
        if not Util.isValidUnsigned(temp):
            # Throw "Invalid Reading"
            Error.throw(0x0103)
        return self._device.readTempC()

    # Returns true if error detected, false
    # if otherwise. Sets critical status to
    # true if error is found. Does not set
    # to false if none is found
    def checkError(self):
        if self.critical_status:
            return True
        status = self._device.readState()
        if status == '':
            return False
        if status == 'openCircuit':
            # Throw "Open Circuit" failure
            Error.throw(0x0104)
        if status == 'shortGND':
            # Throw "GND Short" failure
            Error.throw(0x0105)
        if status == 'shortVCC':
            # Throw "VCC Short" failure
            Error.throw(0x0106)
        if status == 'fault':
            # Throw "General Failure"
            Error.throw(0x0107)

        self.critical_status = True
        return True

    def getValue(self):
        return self.getTemp(), self.getInternalTemp()

    def getDataForPacket(self):
        raw = self.getRawData() >> 4  # Get rid of status bits
        internalTemp = raw & 0x7FF  # Grab last 11 bits (internal temp reading)
        thermocoupleTemp = raw >> 14  # Grab thermocouple reading
        return Util.inttobin((thermocoupleTemp << 11) & internalTemp, 32)
