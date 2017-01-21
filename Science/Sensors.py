import sys
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_GPIO.I2C as I2C
import UV_Sensor as UV
import Thermocouple
import DistanceSensor

PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"
UV_ADDR_LSB = 0x38
DIST_ADDR = 0x52

#Create Sensors
UV_Sens = UV(UV_ADDR_LSB)
Therm = Thermocouple(PinClock, PinChipSel, PinDataIn)
Distance = DistanceSensor(DIST_ADDR)

#Setup Sensors
UV_Sens.setup()
Distance.setup()

print('Press Ctrl-C to quit.')

while True:

    # Read Sensor Data
    time.sleep(0.01)
    temp = Therm.getTemp()
    time.sleep(0.01)
    internal = Therm.getInternalTemp()
    uvData = UV_Sens.getData()

    sys.stdout.write('{0:{fill}16b} ({0}),'.format(uvData, fill='0'))
    #sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S,"))
    #sys.stdout.write('{0:0.2F};'.format(temp))
    sys.stdout.flush()


    #print('    Internal Temperature: {0:0.3F}*C'.format(internal))

    time.sleep(0.25)
