import sys
import time
import UV_Sensor as UV
import Thermocouple
import DistanceSensor
import Limit
import PID
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
import Adafruit_GPIO.GPIO as GPIO

# Define constants
PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"
UV_ADDR_LSB = 0x38
DIST_ADDR = 0x52

# Initialize hardware
ADC.setup()
GPIO = GPIO.AdafruitBBIOAdapter(GPIO.BaseGPIO())


# Create Sensors
UV_Sens = UV.UV(UV_ADDR_LSB)
Therm = Thermocouple.Thermocouple(PinClock, PinChipSel, PinDataIn)
Dist = DistanceSensor.DistanceSensor(DIST_ADDR)
pidCtrl = PID.PID(1, 1, 1)

# Setup Sensors
UV_Sens.setup(2)
Dist.setup()

print('Press Ctrl-C to quit.')


while True:

    # Read Sensor Data
    time.sleep(0.01)
    temp = Therm.getTemp()
    time.sleep(0.01)
    internal = Therm.getInternalTemp()
    uvData = UV_Sens.getData()
    distData = Dist.getRawData()

    # Write data to test
    sys.stdout.write('{0}, '.format(distData))
    #sys.stdout.write('{0}, '.format(pidCtrl.getOutput()))
    #sys.stdout.write('{0:{fill}16b} ({0}),'.format(uvData, fill='0'))
    #sys.stdout.write(time.strftime("%Y-%m-%d %H:%M:%S,"))
    #sys.stdout.write('{0:0.2F};'.format(temp))
    sys.stdout.flush()


    #print('    Internal Temperature: {0:0.3F}*C'.format(internal))

    time.sleep(0.25)