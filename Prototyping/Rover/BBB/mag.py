from Adafruit_I2C import Adafruit_I2C
import time


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

    def read(self):
        print "Beginning read"
        #dataX = i2c.readS16(0x03)
        #dataY = i2c.readS16(0x05)
        #dataZ = i2c.readS16(0x07)
        #print "X: " + str(dataX) + " Y: " + str(dataY) + " Z: " + str(dataZ)
        data = self.i2c.readList(0x1A, 6)
        self.hData = data[1] * 256 + data[0]
        self.rData = data[3] * 256 + data[2]
        self.pData = data[5] * 256 + data[4]
        time.sleep(1)

test = Magnetometer()
while 1:
    test.read()
    print "heading data: " + str(test.hData)
    print test.rData
    print test.pData
    print "heading: " + str(test.hData / 16.0)
