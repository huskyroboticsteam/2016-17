import sys
import time
import Error
import Util
import Parse
import Motor
import Adafruit_BBIO.ADC as ADC  # Ignore compilation errors
from Thermocouple import Thermocouple
from DistanceSensor import DistanceSensor
from Humidity import Humidity
from UV_Sensor import UV
from Encoder import Encoder
from threading import Thread
from CommHandler import CommHandler
from Sensor import SensorHandler
from Packet import Packet, PacketType
from Limit import Limit
from SystemTelemetry import SystemTelemetry
from DrillCtrl import DrillCtrl
from CamFocus import CamFocus
from MoveDrill import MoveDrill
from Command import Command

# Define constants
PinDataIn = "P9_18"
PinChipSel = "P9_17"
PinClock = "P9_22"
UV_ADDR_LSB = 0x38
DIST_ADDR = 0x52
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
Parse.setupParsing()
CommHandling = CommHandler(INTERNAL_IP, INTERNAL_TCP_RECEIVE_PORT)
Packet.setDefaultTarget(MAIN_IP, PRIMARY_TCP_SEND_PORT)
SystemTelemetry.initializeTelemetry()
# Start Communication / Receive Thread
COMMS_THREAD = Thread(target=CommHandling.receiveMessagesOnThread)
COMMS_THREAD.start()

# Create Sensors
UVSensor = UV(UV_ADDR_LSB)
Thermocouple = Thermocouple(PinClock, PinChipSel, PinDataIn)
DistanceSensor = DistanceSensor()
HumiditySensor = Humidity("AIN1")
HumiditySensor.setup(1, 0)  # Setup Humidity Calibration
encoder1 = Encoder("P8_22", "P8_24", 220)
encoder2 = Encoder("P8_28", "P8_30", 220)
encoder3 = Encoder("P8_34", "P8_36", 220)
limit1 = Limit("P8_12")
limit2 = Limit("P8_10")
limit3 = Limit("P8_8")

# Create Motors
DrillMotor = Motor.TalonMC("P8_13")
DrillArmatureMotor = Motor.TalonMC("")
CamFocusServo = Motor.Servo("")
Motor.Motor.enableAll()

# Create Command Interface
drillController = DrillCtrl(DrillMotor, encoder1)
armatureController = MoveDrill(DrillArmatureMotor, DistanceSensor)
camFocusCommand = CamFocus(CamFocusServo)
# Initialize All Commands (Set machine to relaxed state)
Command.initializeAll()

# Add Sensors to handler
SensorHandler.addPrimarySensors(DistanceSensor, UVSensor, Thermocouple, HumiditySensor)
SensorHandler.addAccessorySensors(encoder1, encoder2, encoder3, limit1, limit2, limit3)

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

    # Says everything is okay if there have been no errors on this cycle
    if not Error.areErrors():
        Error.throw(0x00)
    # Clears errors for next cycle
    Error.clearErrors()

    sys.stdout.flush()
    time.sleep(1)
