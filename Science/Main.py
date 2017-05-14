import sys

import Error
import Util
import Parse
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Motor import Motor
from Sensors.Thermocouple import Thermocouple
from Sensors.DistanceSensor import DistanceSensor
from Sensors.Humidity import Humidity
from Sensors.UV_Sensor import UV
from Sensors.Encoder import Encoder
from Sensors.Limit import Limit
from Sensors.Sensor import SensorHandler
from Commands.DrillCtrl import DrillCtrl
from Commands.CamFocus import CamFocus
from Commands.MoveDrill import MoveDrill
from Commands.SystemControl import SystemControl
from Commands.RotateArmature import RotateArmature
from Commands.Command import Command
from CommHandler import CommHandler
from Packet import Packet, PacketType
from SystemTelemetry import SystemTelemetry

# Communication Setup
#MAIN_IP = '192.168.0.1'  # Typical
MAIN_IP = '192.168.0.104'  # Testing on Jaden's machine
PRIMARY_TCP_SEND_PORT = 22
INTERNAL_IP = '192.168.0.90'
INTERNAL_TCP_RECEIVE_PORT = 5000

Packet.setDefaultTarget(MAIN_IP, PRIMARY_TCP_SEND_PORT)

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
CommHandler.setup(INTERNAL_IP, INTERNAL_TCP_RECEIVE_PORT)
Packet.setDefaultTarget(MAIN_IP, PRIMARY_TCP_SEND_PORT)
SystemTelemetry.initializeTelemetry()
CommHandler.startCommsThread()  # Start communication receiving process

# Add Sensors to handler
SensorHandler.addPrimarySensors(DistanceSensor, UVSensor, Thermocouple, HumiditySensor)
SensorHandler.addAccessorySensors(encoder1, encoder2, encoder3, limit1, limit2, limit3)

# Setup and start all sensors
SensorHandler.setupAll()
SensorHandler.startAll()

# Create Command Interface
drillController = DrillCtrl("P8_13", encoder1)
rotateArmature = RotateArmature("P9_16", encoder2)
armatureController = MoveDrill("P8_19", DistanceSensor)
camFocusCommand = CamFocus("P9_14")
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
    CommHandler.addCyclePacket(primarySensorData)

    # Send Auxiliary Sensor Packet
    auxSensorData = Packet(PacketType.AuxSensor)
    auxSensorData.appendData(SensorHandler.getAuxSensorData())
    CommHandler.addCyclePacket(auxSensorData)

    # Send System Telemetry Packet
    SystemTelemetry.updateTelemetry()
    systemPacket = Packet(PacketType.SystemTelemetry)
    systemPacket.appendData(SystemTelemetry.getTelemetryData())
    CommHandler.addCyclePacket(systemPacket)

    sys.stdout.flush()
