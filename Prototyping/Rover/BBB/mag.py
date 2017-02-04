from Adafruit_I2C import Adafruit_I2C
import time

# TODO: shorten startup time if possible
class Magnetometer:
    def __init__(self):
        address = 0x28
        self.i2c = Adafruit_I2C(address, -2)
        time.sleep(1)

        chip_id = self.i2c.readU8(0x00)
        print "chipID:  " + str(chip_id)
        time.sleep(1)

        self.i2c.write8(0x3D, 0x09)
        time.sleep(1)

    # returns the heading data or -1 if an error occurs
    def read(self):
        print "Beginning read"
        try:
            data = self.i2c.readList(0x1A, 6)
            self.hData = data[1] * 256 + data[0]
            self.rData = data[3] * 256 + data[2]
            self.pData = data[5] * 256 + data[4]
            return self.hData / 16.0
        except RuntimeError:
            return -1

