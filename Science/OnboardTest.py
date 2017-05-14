import sys

import Util
from Sensors.Thermocouple import Thermocouple
from Sensors.DistanceSensor import DistanceSensor
from Sensors.UV_Sensor import UV

dist = DistanceSensor()
therm = Thermocouple("P9_22", "P9_17", "P9_18")
uv = UV(0x38)

def testUV():
    uv.setup()
    Util.write(uv.getValue())

def decodeUV():
    bytes = uv.getDataForPacket()
    Util.write(bytes)
    val = Util.bytesToInt(bytes)
    Util.write(val)

def testDistanceSensor():
    dist.start()
    Util.write(dist.getValue())
    Util.write(dist.getDataForPacket())

def decodeDistanceSensor():
    bytes = dist.getDataForPacket()
    Util.write(Util.bytesToInt(bytes))

def testThermocouple():
    # Thermocouple Internal Temp
    Util.write("Internal Temp: ")
    Util.write(therm.getInternalTemp())
    # Thermocouple External Temp
    Util.write("External Temp: ")
    Util.write(therm.getTemp())
    # Thermocouple Error
    Util.write("Error: ")
    Util.write(therm.checkError())
    # Data
    Util.write("Data: ")
    Util.write(therm.getValue())
    # Packet Val
    Util.write("Packet Val: ")
    Util.write(therm.getDataForPacket())

def decodeTherm():
    data = therm.getDataForPacket()
    intData = Util.bytesToInt(data)
    temp = (intData & 0xFFFF0000) >> 16
    tempInt = intData & 0x0000FFFF
    Util.write("Got Temp: ")
    Util.write((temp*0.25))
    Util.write("Got Internal Temp: ")
    Util.write((tempInt*0.0625))

testUV()
decodeUV()