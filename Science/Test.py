import Error
import sys
import socket
import time
import math
import Util
import threading
import Parse
from Packet import Packet, CameraID, AuxCtrlID, PacketType
from SystemTelemetry import SystemTelemetry
from CommHandler import Message

LISTEN = False

# BBB TCP IP / PORT
Packet.DEF_TARGET_IP = '192.168.0.90' 
Packet.DEF_TARGET_PORT = 5000

def testParsing():
    Parse.setupParsing()
    parsingThread = threading.Thread(target=Parse.thread_parsing)
    parsingThread.start()
    mes = Message(b'axbd\x81\x01zvgh', '192.168.0.1')
    Parse.queueMessage(mes)

def testPacket():
    pack = Packet(0x72)
    pack.appendData('\x4e')
    pack.appendData(Util.long_to_bytes(45))
    # Data value = 0x4E2D , 20,013
    pack.send()

"""
Sends command to the BBB
Only works for Aux and Sys Ctrl
* Img Request Different (See requestImage())
Per Documentation for cmdTyp:
    0x81 = Aux Ctrl
    0x82 = Sys Ctrl
Or import Packet.PacketType and use as enum
"""
def sendCommand(cmdTyp, cmdID, cmdVal):
    pack = Packet(cmdTyp)
    data = _getCommandData(cmdID, cmdVal)
    pack.appendData(data)
    pack.send()


"""
Parses given data into appropriate CmdID + CmdVal bytes
"""
def _getCommandData(cmdID, cmdVal):
    cmdBytes = Util.long_to_bytes(cmdID)
    cmdValBytes = Util.long_to_bytes(cmdVal)
    
    if len(cmdBytes) == 0:
        # Error ?? 
        pass
    elif len(cmdBytes) != 1:
        cmdBytes = cmdBytes[0]

    if len(cmdValBytes) > 4:
        cmdValBytes = cmdValBytes[0:4]
    elif len(cmdValBytes) < 4:
        cmdValBytes += Util.long_to_bytes(0) * (4 - len(cmdValBytes))

    return cmdBytes + cmdValBytes

"""
Asks BBB for image
"""
def requestImage(camID):
    #pack = Packet(PacketType.ImageRequest)
    data = Util.long_to_bytes(Parse.IMG_REQ_CONST)  # Turns img request into bytes
    camID = Util.long_to_bytes(camID)  # Turns camID into bytes
    
    if len(camID) > 1:
        camID = camID[0]
    elif len(camID) < 1:
        camID = Util.long_to_bytes(0x01)  # Default to cam ID 1
    
    Util.write(data + camID)

    pack.appendData(data + camID)
    pack.send()


def testTelemetry():
    SystemTelemetry.initializeTelemetry()
    SystemTelemetry.updateTelemetry()
    tel = SystemTelemetry.getTelemetryData()
    c = 0
    Util.write(str(Util.bytesToInt(tel, 6, 8)))  # Prints number of active threads


# Test Telemetry
# testTelemetry()

# Test Image Request
# requestImage(CameraID.Microscope)

# Test command sending
# sendCommand(PacketType.AuxControl, AuxCtrlID.CamFocusPos, 90)

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if LISTEN:
    SOCKET.bind(('192.168.0.1', 22))
    while True:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("Data Received: " + str(data) + "\nFrom: " + str(clientAddr))
            