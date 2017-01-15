import sys
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.I2C as I2C
import Adafruit_MAX31855.MAX31855 as MAX31855

PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"

thermocouple = MAX31855.MAX31855(PinClock, PinChipSel, PinDataIn) # spi=SPI.SpiDev(1,0)) #

print('Press Ctrl-C to quit.')

while True:

    time.sleep(0.01)
    temp = thermocouple.readTempC()
    time.sleep(0.01)
    internal = thermocouple.readInternalC()

    sys.stdout.write(UVSensor.readByte(0x71))
    sys.stdout.write(UVSensor.readByte(0x73))
    #print('Thermocouple Temperature: {0:0.3F}*C'.format(temp))

    #print('{0:0.2F},'.format(temp), end='')
    sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S,"))
    sys.stdout.write('{0:0.2F};'.format(temp))
    sys.stdout.flush()

    #print('    Internal Temperature: {0:0.3F}*C'.format(internal))

    time.sleep(0.25)

# #/dev/spidev1.0

#GPIO.setup(PinDataIn, GPIO.IN)
