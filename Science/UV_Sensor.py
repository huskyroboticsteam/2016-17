"""
Reads a UV Sensor board through I2C

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
This code has been tested.
"""
import Util
import Error
import Adafruit_GPIO.I2C as I2C
from Sensor import Sensor


class UV(Sensor):

    # default time constant
    _uvTConst = 0x02
    critical_status = False

    # initialize device with the correct LSB address given in the
    # documentation.
    def __init__(self, LSB_ADDR):
        self._uvl = None
        self._uvm = None
        try:
            self._uvl = I2C.Device(LSB_ADDR, I2C.get_default_bus())
            self._uvm = I2C.Device(LSB_ADDR + 1, I2C.get_default_bus())
        except:
            # Throw "Communication Failure"
            self.critical_status = True
            Error.throw(0x0203, "Could not initialize UV Sensor communications")
        self.setup(self._uvTConst)

    # Sets up device with time constant
    def setup(self, tConst=_uvTConst):  # tConst = 0, 1, 2, 3
        if not self.critical_status:
            self._uvTConst = tConst & 3  # Removes any unwanted digits
            self._uvl.writeRaw8((self._uvTConst << 2) | 2)  # Writes to correct register

    # Reads raw binary value from the register
    def getRaw(self):
        uvData = 0
        if self.critical_status:
            return 0
        try:
            uvData = self._uvl.readRaw8()
            uvData |= self._uvm.readRaw8() << 8
        except:
            # Throw "Could Not Get Reading"
            Error.throw(0x0201)
        if not Util.isValidUnsigned(uvData):
            # Throw "Reading Invalid"
            Error.throw(0x0202)
        return uvData

    # Gets data in uW/cm/cm
    def getValue(self):
        return self.getRaw() * 5  # uW/cm/cm (multiplication factor of 5 given by the datasheet)

    def getDataForPacket(self):
        return Util.byteMap(self.getValue(), 32)



