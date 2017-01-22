import Adafruit_GPIO.I2C as I2C


class UV(object):

    _uvTConst = 0x02

    def __init__(self, LSB_ADDR):
        self._uvl = I2C.Device(LSB_ADDR, I2C.get_default_bus())
        self._uvm = I2C.Device(LSB_ADDR + 1, I2C.get_default_bus())

    def setup(self, tConst): # tConst = 0, 1, 2, 3
        _uvTConst = tConst & 3
        self._uvl.writeRaw8((_uvTConst << 2) | 2)

    def getRaw(self):
        uvData = self._uvl.readRaw8()
        uvData |= self._uvm.readRaw8() << 8
        return uvData

    def getData(self):
        return self.getRaw() * 5  # uW/cm/cm
