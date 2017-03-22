"""
Packet Handler wrapper.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import socket
import time
from Error import Error
from Util import Util


class Packet:

    RECEIVE_BYTE_SIZE = 1024

    DEF_TARGET_IP = '192.168.0.10'
    DEF_TARGET_PORT = 24

    def __init__(self, id=0x00, targetIP=DEF_TARGET_IP, targetPort=DEF_TARGET_PORT):
        self._data = ""
        self._id = id
        self._recieved = ""
        self._targetIP = targetIP
        self._targetPort = targetPort

    # Appends 32bit UNIX timestamp to beginning of packet
    def addTimeID(self):
        timestamp = Util.inttobin(time.time(), 32)
        id = Util.inttobin(self._id)
        self._data = timestamp + id + self._data

    # Append bitwise list to current packet buffer
    # EG [0,1,1,0]
    def appendData(self, data):
        self._data += str(data)

    def getRecieved(self):
        return self._recieved

    # Clear buffer
    def clear(self):
        self._data = ""

    # Sends data to constructor-specified client
    def send(self):
        try:
            self.addTimeID()  # Always add time and id to the packet
            s = socket.socket()
            s.connect((self._targetIP, self._targetPort))
            s.send(self._data)
            s.close()
        except socket.error:
            # Throw "Failed to send packet"
            Error.throw(0x0503)

    @classmethod
    def setDefaultTarget(cls, targetIP, targetPort):
        cls.DEF_TARGET_IP = targetIP
        cls.DEF_TARGET_PORT = targetPort


# Packet Type Enumeration:


class PacketType:
    PrimarySensor = 0x00
    Error = 0x01
    AuxSensor = 0x02
    SystemTelemetry = 0x03
    ImageRequest = 0x80
    AuxControl = 0x81
    SysControl = 0x82

