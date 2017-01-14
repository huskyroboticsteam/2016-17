import time
#import Adafruit_BBIO.GPIO as GPIO
#from Adafruit_BBIO.SPI import SPI
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.I2C as I2C
import Adafruit_MAX31855.MAX31855 as MAX31855

#spi = SPI(0,0)

PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"

I2C_SDAPin = "P9_20"
I2C_SCLPin = "P9_19"

thermocouple = MAX31855.MAX31855(PinClock, PinChipSel, PinDataIn) # spi=SPI.SpiDev(1,0)) #

print('Press Ctrl-C to quit.')

while True:

    time.sleep(0.01)
    temp = thermocouple.readTempC()
    time.sleep(0.01)
    internal = thermocouple.readInternalC()

    print('Thermocouple Temperature: {0:0.3F}*C'.format(temp))

    print('    Internal Temperature: {0:0.3F}*C'.format(internal))

    time.sleep(1.0)

# #/dev/spidev1.0

#GPIO.setup(PinDataIn, GPIO.IN)