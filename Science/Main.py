import sys
import time
import UV_Sensor as UV
from Thermocouple import Thermocouple
from DistanceSensor import DistanceSensor
from Humidity import Humidity
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
import Encoder
from threading import Thread
import CommHandler as Comms
from Sensor import SensorHandler

# Define constants
PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"
UV_ADDR_LSB = 0x38
DIST_ADDR = 0x52

# Communication Setup
MAIN_IP = '192.168.0.10'
PRIMARY_TCP_SEND_PORT = 24
INTERNAL_IP = '127.0.0.1'
INTERNAL_TCP_RECEIVE_PORT = 5000

# Initialize hardware
ADC.setup()
CommHandling = Comms.CommHandler(INTERNAL_IP, INTERNAL_TCP_RECEIVE_PORT)

# Start Communication Thread
COMMS_THREAD = Thread(target=CommHandling.receiveMessagesOnThread)
COMMS_THREAD.start()

# Create Sensors
UVSensor = UV.UV(UV_ADDR_LSB)
Thermocouple = Thermocouple(PinClock, PinChipSel, PinDataIn)
DistanceSensor = DistanceSensor()
HumiditySensor = Humidity(1)
# Need to write in the actual pin values here.
encoder1 = Encoder.Encoder("PINA", "PINB", 220)
encoder2 = Encoder.Encoder("PINA", "PINB", 220)
encoder3 = Encoder.Encoder("PINA", "PINB", 220)

# Add Sensors to handler
SensorHandler.addPrimarySensors(UVSensor,
                               Thermocouple,
                               DistanceSensor,
                               HumiditySensor)
SensorHandler.addAccessorySensors(encoder1,
                                  encoder2,
                                  encoder3)

# Setup and start all sensors
SensorHandler.setupAll()
SensorHandler.startAll()


while True:

    # Update Sensor Data
    SensorHandler.updateAll()
    sys.stdout.write('{0}'.format(SensorHandler.getDataArray()))

    sys.stdout.flush()
    CommHandling.sendAll()
    time.sleep(1)
