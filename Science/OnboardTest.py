import sys

import Util
from Sensors.Thermocouple import Thermocouple
from Sensors.DistanceSensor import DistanceSensor

dist = DistanceSensor()
therm = Thermocouple("P9_22", "P9_17", "P9_18")

def testDistanceSensor():
    dist.start()
    Util.write(dist.getValue())
    Util.write(dist.getDataForPacket())

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

testDistanceSensor()