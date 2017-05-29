import sys
import time
import socket
from threading import Thread
import Error
import Util
import Parse
from Packet import Packet, PacketType
from SystemTelemetry import SystemTelemetry

LISTEN = True

TCP_SEND_ADDR = '192.168.0.90'
TCP_SEND_PORT = 5000

Packet.setDefaultTarget(TCP_SEND_ADDR, TCP_SEND_PORT)

def sendThing():
    i = 0
    while True:
        
        time.sleep(10)
        pack = Packet(0x81)

        cmdID = 3
        data = Util.long_to_byte_length(cmdID, 1)

        pos = 90
        data += Util.long_to_byte_length(pos, 4)

        pack.appendData(data)
        pack.send()
        sys.stdout.write("PACKET SENT to POS " + str(pos) + "\n")
        i += 1

picT = Thread(target=sendThing)
picT.start()

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if LISTEN:
    SOCKET.bind(('192.168.0.101', 5000))
    while True:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
