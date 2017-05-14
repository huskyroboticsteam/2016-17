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

def sendPicReq():

    time.sleep(10)

    pack = Packet(0x80)

    camReqInt = 0x492063616E2068617A20706963747572653F02
    camReqByte = Util.long_to_byte_length(camReqInt, 24)

    pack.appendData(camReqByte)

    pack.send()

picT = Thread(target=sendPicReq)
picT.start()

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if LISTEN:
    SOCKET.bind(('192.168.0.104', 22))
    while True:
        SOCKET.listen(1)
        client, clientAddr = SOCKET.accept()
        data = client.recv(1024)
        sys.stdout.write("\nData Received: " + str(data) + "\n\tFrom: " + str(clientAddr))
