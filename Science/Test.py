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

TEST_IP = '127.0.0.1'
TEST_PORT = 22
LISTEN = False

def testParsing():
    Parse.setupParsing()
    parsingThread = threading.Thread(target=Parse.thread_parsing)
    parsingThread.start()
    mes = Message(b'axbd\x81\x01zvgh', '192.168.0.1')
    Parse.queueMessage(mes)

def testPacket():
    pack = Packet(0x00)
    pack.appendData('\x4e')
    pack.appendData(Util.long_to_bytes(45))
    # Data value = 0x4E2D , 20,013
    pack.send()


SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCKET.bind((TEST_IP, TEST_PORT))

if LISTEN:
        while True:
            SOCKET.listen(1)
            client, clientAddr = SOCKET.accept()
            data = client.recv(1024)
            sys.stdout.write("Data Received: " + str(data) + "\nFrom: " + str(clientAddr))
            