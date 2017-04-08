import Error
import sys
import socket
import time
import Util
import threading
from Packet import Packet
from SystemTelemetry import SystemTelemetry
from TalonMC import TalonMC

def snedTestPacket():
    time.sleep(1)
    testPacket = Packet(0x03, '192.168.0.1', 24)
    testPacket.appendData(SystemTelemetry.getTelemetryData())
    testPacket.send()
    time.sleep(3)

def parsePacket(packetData):
    packetData = Util.chartobytes(packetData)
    sys.stdout.write(packetData)
    packetTimestamp = int(packetData[0:32], 2)
    packetID = int(packetData[33:40], 2)
    return "Timestamp: " + str(packetTimestamp) + "  |  ID: " + str(packetID)

# snedThread = threading.Thread(target=snedTestPacket)
# snedThread.start()

"""
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind(('192.168.0.1', 24))
while True:
    try:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("Received: {0}\n".format(data))
        sys.stdout.write("\n" + parsePacket(data) + "\n")
    except socket.error:
        pass
"""

"""
DrillMotor = TalonMC("P8_13")
DrillMotor.setFreq(10000)
x = 0.0
while x < 1.0:
    DrillMotor.set(x)
    x += 0.1
    time.sleep(0.8)
DrillMotor.set(0.0)
"""
