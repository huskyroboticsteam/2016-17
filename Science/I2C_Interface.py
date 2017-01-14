from Adafruit_GPIO import I2C

class I2C_Interface:

    def __init__(self, address=0x77):
        self._I2C = I2C.Device(address, 0)

    def getI2C(self):
        return self._I2C

    def readByte(self, register):
        return self._I2C.readS8(register)