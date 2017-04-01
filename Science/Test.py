import Error
import sys
import socket
import time
import Util
import threading
from Packet import Packet
from SystemTelemetry import SystemTelemetry


def snedTestPacket():
    time.sleep(1)
    testPacket = Packet(0x02, '192.168.0.1', 24)
    testPacket.appendData(SystemTelemetry.getTelemetryData())
    testPacket.send()
    time.sleep(3)
    Error.throw(0x0503)

def parsePacket(packetData):
    packetData = Util.chartobytes(packetData)
    packetTimestamp = int(packetData[0:32], 2)
    packetID = int(packetData[33:40], 2)
    return "Timestamp: " + str(packetTimestamp) + "  |  ID: " + str(packetID)

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind(('192.168.0.1', 24))
while True:
    try:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("Received: {0}\n".format(data))
        sys.stdout.write("\n" + Util.inttobin(parsePacket(data)) + "\n")
    except socket.error:
        pass

