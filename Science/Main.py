import sys
import Error
import Util
import Parse
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Motor import Motor
from Thermocouple import Thermocouple
from DistanceSensor import DistanceSensor
from Humidity import Humidity
from UV_Sensor import UV
from Encoder import Encoder
from CommHandler import CommHandler
from Sensor import SensorHandler
from Packet import Packet, PacketType
from Limit import Limit
from SystemTelemetry import SystemTelemetry
from DrillCtrl import DrillCtrl
from CamFocus import CamFocus
from MoveDrill import MoveDrill
from SystemControl import SystemControl
from RotateArmature import RotateArmature
from Command import Command

# Communication Setup
MAIN_IP = '192.168.0.1'
PRIMARY_TCP_SEND_PORT = 24
INTERNAL_IP = '127.0.0.1'
INTERNAL_TCP_RECEIVE_PORT = 5000

# Initialize hardware and communications
try:
    ADC.setup()
    Util.setADC_Status(True)
except:
    # Throw "ADC Could not initialize"
    Error.throw(0x0001, "Failed to initialize ADC")

# Create Sensors
UVSensor = UV(0x38)
Thermocouple = Thermocouple("P9_22", "P9_17", "P9_18")
DistanceSensor = DistanceSensor()
HumiditySensor = Humidity("AIN1")
HumiditySensor.setup(1, 0)  # Setup Humidity Calibration
encoder1 = Encoder("P8_22", "P8_24", 220)
encoder2 = Encoder("P8_28", "P8_30", 220)
encoder3 = Encoder("P8_34", "P8_36", 220)
limit1 = Limit("P8_12")
limit2 = Limit("P8_10")
limit3 = Limit("P8_8")

Parse.setupParsing()
CommHandling = CommHandler(INTERNAL_IP, INTERNAL_TCP_RECEIVE_PORT)
Packet.setDefaultTarget(MAIN_IP, PRIMARY_TCP_SEND_PORT)
SystemTelemetry.initializeTelemetry()
CommHandling.startCommsThread()  # Start communication receiving process

# Add Sensors to handler
SensorHandler.addPrimarySensors(DistanceSensor, UVSensor, Thermocouple, HumiditySensor)
SensorHandler.addAccessorySensors(encoder1, encoder2, encoder3, limit1, limit2, limit3)

# Setup and start all sensors
SensorHandler.setupAll()
SensorHandler.startAll()

# Create Command Interface
drillController = DrillCtrl("P8_13", encoder1)
rotateArmature = RotateArmature("P8_46", encoder2)
armatureController = MoveDrill("P8_19", DistanceSensor)
camFocusCommand = CamFocus("P8_45")
systemControl = SystemControl("P9_15")

# Initialize All Commands (Set machine to relaxed state)
Command.initializeAll()
# Start All Commands
Command.startAll()

# Enable all Motors
Motor.enableAll()

while True:

    # Update All Sensor Data In Main Thread
    SensorHandler.updateAll()

    # Send Primary Sensor Packet
    primarySensorData = Packet(PacketType.PrimarySensor)
    primarySensorData.appendData(SensorHandler.getPrimarySensorData())
    CommHandling.addCyclePacket(primarySensorData)

    # Send Auxiliary Sensor Packet
    auxSensorData = Packet(PacketType.AuxSensor)
    auxSensorData.appendData(SensorHandler.getAuxSensorData())
    CommHandling.addCyclePacket(auxSensorData)

    # Send System Telemetry Packet
    SystemTelemetry.updateTelemetry()
    systemPacket = Packet(PacketType.SystemTelemetry)
    systemPacket.appendData(SystemTelemetry.getTelemetryData())
    CommHandling.addCyclePacket(systemPacket)

    CommHandling.sendAll()

    sys.stdout.flush()
