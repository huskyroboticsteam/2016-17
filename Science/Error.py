import sys
import Packet
import Util
from CommHandler import CommHandler


errors = []


def clearErrors():
    errors = []


def throw(errorCode, comment="", fatal=False):
    if len(comment) > 0:
        comment = " Given information: " + str(comment) + "\n"
    sys.stderr.write("Error: " + str(errorCode) + " | Refer to documentation for more information.\n" + comment + "\n")
    errors.append(errorCode)
    errorPack = Packet.Packet(Packet.PacketType.Error)
    errorPack.appendData(Util.inttobin(errorCode, 16))
    CommHandler.sendAsyncPacket(errorPack)
    if fatal:
        sys.exit(0x00FF)


def getErrors():
    return errors


def areErrors():
    return len(errors) > 0
