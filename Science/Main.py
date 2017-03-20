import sys
import time
import UV_Sensor as UV
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Thermocouple import Thermocouple
from DistanceSensor import DistanceSensor
from Humidity import Humidity
from Encoder import Encoder
from threading import Thread
from CommHandler import CommHandler
from Sensor import SensorHandler
from Packet import Packet, PacketType
from Error import Error
from Limit import Limit
from SystemTelemetry import SystemTelemetry

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

# Initialize hardware and communications
ADC.setup()
CommHandling = CommHandler(INTERNAL_IP, INTERNAL_TCP_RECEIVE_PORT)
Packet.setDefaultTarget(MAIN_IP, PRIMARY_TCP_SEND_PORT)
SystemTelemetry.initializeTelemetry()
# Start Communication / Receive Thread
COMMS_THREAD = Thread(target=CommHandling.receiveMessagesOnThread)
COMMS_THREAD.start()

# Create Sensors
UVSensor = UV.UV(UV_ADDR_LSB)
Thermocouple = Thermocouple(PinClock, PinChipSel, PinDataIn)
DistanceSensor = DistanceSensor()
HumiditySensor = Humidity(1)
# Need to write in the actual pin values here.
encoder1 = Encoder("PINA", "PINB", 220)
encoder2 = Encoder("PINA", "PINB", 220)
encoder3 = Encoder("PINA", "PINB", 220)
limit1 = Limit("PINA")
limit2 = Limit("PINA")
limit3 = Limit("PINA")

# Add Sensors to handler
SensorHandler.addPrimarySensors(DistanceSensor,
                               UVSensor,
                               Thermocouple,
                               HumiditySensor)
SensorHandler.addAccessorySensors(encoder1,
                                  encoder2,
                                  encoder3,
                                  limit1,
                                  limit2,
                                  limit3)

# Setup and start all sensors
SensorHandler.setupAll()
SensorHandler.startAll()


while True:

    # Update All Sensor Data In Main Thread
    SensorHandler.updateAll()

    # Send Primary Sensor Packet
    primarySensorData = Packet(PacketType.PrimarySensor)
    primarySensorData.appendData(SensorHandler.getPrimarySensorData())
    CommHandling.addCyclePacket(primarySensorData)

    # Send Auxillary Sensor Packet
    auxSensorData = Packet(PacketType.AuxSensor)
    auxSensorData.appendData(SensorHandler.getAuxSensorData())
    CommHandling.addCyclePacket(auxSensorData)

    # Send System Telemetry Packet
    SystemTelemetry.updateTelemetry()
    systemPacket = Packet(PacketType.SystemTelemetry)
    systemPacket.appendData(SystemTelemetry.getTelemetryData())
    CommHandling.addCyclePacket(systemPacket)

    CommHandling.sendAll()

    # Says everything is okay if there have been no errors on this cycle
    if not Error.areErrors():
        Error.throw(0x00)
    # Clears errors for next cycle
    Error.clearErrors()

    sys.stdout.flush()
    time.sleep(1)
