import sys
import Adafruit_GPIO.I2C as I2C


dev = I2C.Device(0x38, I2C.get_default_bus())
print (2<<2) | 2
dev.writeRaw8((2<<2) | 2)