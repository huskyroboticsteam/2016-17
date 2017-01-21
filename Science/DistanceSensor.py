import Adafruit_GPIO.I2C as I2C


class DistanceSensor(object):

    def __init__(self, addr):
        self._addr = addr
        self._i2cDev = I2C.Device(self._addr, I2C.get_default_bus())

    def setup(self):
        return 0

    def getData(self):
        return 0