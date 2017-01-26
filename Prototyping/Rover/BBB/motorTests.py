from Adafruit_I2C import Adafruit_I2C
from time import time

i2c = Adafruit_I2C(0x60, 1)
for i in range(0x40):
    i2c.write8(i, 0x00)
'''
for i in range(0x26, 0x2A):
    for j in range(0x2A, 0x2E):
        for k in range(0x2E, 0x32):
            i2c.write8(i, 0xFF)
            i2c.write8(j, 0xFF)
            i2c.write8(k, 0xFF)
        for a in range(0x40):
            i2c.write8(a, 0x00)


i2c.write8(0x27, 0x1F)
i2c.write8(0x2B, 0x0F)
i2c.write8(0x2D, 0x1F)
i2c.write8(0x31, 0x0F)
i2c.write8(0x33, 0x1F)
'''

def set_pwm(channel, on, off):
    i2c.write8(0x06 + 4 * channel, on & 0xFF)
    i2c.write8(0x07 + 4 * channel, on >> 8)
    i2c.write8(0x08 + 4 * channel, off & 0xFF)
    i2c.write8(0x09 + 4 * channel, off >> 8)

set_pwm(8, 0, 0xFF)
set_pwm(9, 0x00, 0xFF)
set_pwm(10, 0x1, 0x00)

for i in range(0x40):
    print str(hex(i)) + ": " + str(hex(i2c.readU8(i)))
'''
print i2c.readList(0x20, 0x10)
for i in range(0XFF):
    i2c.write8(i, 0x00)
    #time.sleep(.1)
    print i
    print i2c.readU8(i)
#i2c.write8(0x2A, 0x1)
print i2c.readList(0x20, 0x10)
'''