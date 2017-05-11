import Error
import sys
import socket
import time
import math
import Util
import threading
import Parse
from Packet import Packet
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
Sends auxilliary command to the BBB
"""
def sendAuxCommand(cmdID, cmdVal):
    pack = Packet(0x81)
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


SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if LISTEN:
    SOCKET.bind(('192.168.0.1', 22))
    while True:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("Data Received: " + str(data) + "\nFrom: " + str(clientAddr))
            