"""
Packet Handler wrapper.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Tested as of 3/26/2017)

"""
import socket
import time
import Error
import Util

CONNECTION_STATUS = True


class Packet:

    RECEIVE_BYTE_SIZE = 1024
    DEFAULT_TARGET_IP = '192.168.0.1'
    DEFAULT_TARGET_PORT = 24

    def __init__(self, id=0x00, targetIP=None, targetPort=None):
        self._data = ""
        self._id = id
        self._recieved = ""
        if targetPort == None:
            targetIP = self.DEF_TARGET_IP
            targetPort = self.DEF_TARGET_PORT
        elif targetIP == None:
            targetIP = self.DEF_TARGET_IP
        self._targetIP = targetIP
        self._targetPort = targetPort

    # Appends 32bit UNIX timestamp to beginning of packet
    def addTimeID(self):
        timestamp = Util.inttobin(int(time.time()), 32)
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
    # Returns whether or not send is successful
    def send(self):
        if self._data == Util.inttobin(0x0503, 16) and not getConnectionStatus():
            return False
        try:
            self.addTimeID()  # Always add time and id to the packet
            s = socket.socket()
            s.connect((self._targetIP, self._targetPort))
            s.send(Util.full_bin_to_chr(self._data))
            s.close()
        except socket.error:
            # Throw "Failed to send packet"
            Error.throw(0x0503, "Failed to send packet", "Packet.py", 58)
            setStatus(False)
            return False
        setStatus(True)
        return True

    def getData(self):
        return self._data

    @classmethod
    def setDefaultTarget(cls, targetIP, targetPort):
        cls.DEF_TARGET_IP = targetIP
        cls.DEF_TARGET_PORT = targetPort
        time.sleep(0.03)


# Packet Type Enumeration:


class PacketType:
    PrimarySensor = 0x00
    Error = 0x01
    AuxSensor = 0x02
    SystemTelemetry = 0x03
    ImageRequest = 0x80
    AuxControl = 0x81
    SysControl = 0x82


class AuxCtrlID:
    MoveDrill = 0x00
    DrillRPM = 0x01
    CamFocusPos = 0x02
    RotateArmature = 0x03

class CameraID:
    Microscope = 0x00

class SysCtrlID:
    Ping = 0x00
    Reboot = 0x01


def setStatus(status):
    global CONNECTION_STATUS
    CONNECTION_STATUS = status


def getConnectionStatus():
    global CONNECTION_STATUS
    return CONNECTION_STATUS