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
            Error.throw(0x0108, "Could not initialize thermocouple communications")
            self.critical_status = True
        self.checkError()

    def getRawData(self):
        self.checkError()
        if self.critical_status:
            return 0
        raw = 0
        try:
            raw = self._device._read32()
        except:
            Error.throw(0x0108, "Could not initialize thermocouple communications")
        return raw

    def getInternalTemp(self):  # degrees C
        self.checkError()
        if self.critical_status:
            return 0
        time.sleep(0.01)
        internal_temp = 0
        try:
            internal_temp = self._device.readInternalC()
        except:
            Error.throw(0x0102, "Could not get internal temperature reading")
        if not Util.isValidUnsigned(internal_temp):
            Error.throw(0x0103, "Internal temperature reading invalid")
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
            Error.throw(0x0101, "Could not get external temperature reading")
        if not Util.isValidUnsigned(temp):
            Error.throw(0x0103, "External temperature reading invalid")
        return self._device.readTempC()

    # Returns true if error detected, false
    # if otherwise. Sets critical status to
    # true if error is found. Does not set
    # to false if none is found
    def checkError(self):
        status = self._device.readState()
        if status == '':
            return False
        if status == 'openCircuit':
            Error.throw(0x0104, "Open Circuit detected on Thermocouple.")
        if status == 'shortGND':
            Error.throw(0x0105, "Ground short detected on Thermocouple.")
        if status == 'shortVCC':
            Error.throw(0x0106, "VCC short detected on Thermocouple.")
        if status == 'fault':
            Error.throw(0x0107, "General failure on Thermocouple.")

        self.critical_status = True
        return True

    def getValue(self):
        return self.getTemp(), self.getInternalTemp()

    def getDataForPacket(self):
        raw = self.getRawData() >> 4  # Get rid of status bits
        internalTemp = raw & 0x7FF  # Grab last 11 bits (internal temp reading)
        thermocoupleTemp = raw >> 14  # Grab thermocouple reading
        return Util.byteMap((thermocoupleTemp << 11) & internalTemp, 32)  # BYTEMAP?

