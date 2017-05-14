import sys
import os
import Util
from CommHandler import CommHandler
from Packet import Packet
from Packet import PacketType
from Packet import getConnectionStatus, setStatus


errors = []


def clearErrors():
    global errors
    errors = []


def throw(errorCode, comment="", file="", line=None, fatal=False):
    if not getConnectionStatus() and errorCode == 0x0503:
        return False
    elif errorCode == 0x0503:
        comment += "\nCHECK ETHERNET CABLE ATTACHMENT \n"
        setStatus(False)
    if len(comment) > 0:
        comment += "\n\tGiven information: " + str(comment) + "\n"
    if file != "":
        comment += "File: " + file
    if not (line is None):
        comment += " | " + "Line: " + str(line)
    comment += "\n"
    error_out = "Error: " + hex(errorCode) + " | Refer to documentation for more information.\n" + comment + "\n"
    sys.stderr.write(error_out)
    errors.append(errorCode)
    errorPack = Packet(PacketType.Error)
    errorPack.appendData(Util.byteMap(errorCode, 16))  # BYTEMAP?
    CommHandler.sendAsyncPacket(errorPack)
    errorPack = None
    if fatal:
        os.system("sudo reboot")  # TODO: Test whether or not this works.
        sys.exit(0x00FF)


def getErrors():
    return errors


def areErrors():
    return len(errors) > 0
