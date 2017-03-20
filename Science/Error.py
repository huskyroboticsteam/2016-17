from Packet import Packet, PacketType
from Util import Util
from CommHandler import CommHandler


class Error:

    errors = []

    @classmethod
    def clearErrors(cls):
        cls.errors = []

    @classmethod
    def throw(cls, errorCode):
        cls.errors.append(errorCode)
        errorPack = Packet(PacketType.Error)
        errorPack.appendData(Util.inttobin(errorCode, 16))
        CommHandler.sendAsyncPacket(errorPack)

    @classmethod
    def getErrors(cls):
        return cls.errors

    @classmethod
    def areErrors(cls):
        return len(cls.errors) > 0