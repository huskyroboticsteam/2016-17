import sys
import Util
import Motor
from Packet import Packet
from Packet import PacketType
from Packet import getConnectionStatus
from CommHandler import CommHandler


errors = []


def clearErrors():
    errors = []


def throw(errorCode, comment="", file="", line=None, fatal=False):
    if not getConnectionStatus() and errorCode == 0x0503:
        return False
    elif errorCode == 0x0503:
        comment += "CHECK ETHERNET CABLE ATTACHMENT \n"
    if len(comment) > 0:
        comment += " Given information: " + str(comment) + "\n"
    if file != "":
        comment += "File: " + file
    if not (line is None):
        comment += " | " + "Line: " + str(line)
    comment += "\n"
    error_out = "Error: " + hex(errorCode) + " | Refer to documentation for more information.\n" + comment + "\n"
    sys.stderr.write(error_out)
    errors.append(errorCode)
    errorPack = Packet(PacketType.Error)
    errorPack.appendData(Util.inttobin(errorCode, 16))
    CommHandler.sendAsyncPacket(errorPack)
    if fatal:
        Motor.Motor.stopAll()
        sys.exit(0x00FF)


def getErrors():
    return errors


def areErrors():
    return len(errors) > 0
