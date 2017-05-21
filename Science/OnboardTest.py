import sys
import Util
import Error
import Adafruit_BBIO.ADC as ADC
from Sensors.Encoder import Encoder

test = Encoder("P8_14", "P8_16", 220)

for n in range(0, 10000):
    Util.write(test.getValue())

"""
ADC.setup()
dist = DistanceSensor()
therm = Thermocouple("P9_22", "P9_17", "P9_18")
uv = UV(0x38)
moist = Humidity("AIN1")
limTest = Limit("P8_12")

def testLim():
    Util.write(limTest.getValue())

def decodeLim():
    val = limTest.getDataForPacket()
    intData = Util.bytesToInt(val)
    Util.write(intData)

def testMoisture():
    Util.write(moist.getValue())

def decodeMoisture():
    data = moist.getDataForPacket()
    intData = Util.bytesToInt(data)
    Util.write(intData / 1023.0)
    
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

#testUV()
#decodeUV()

"""