"""
TCP/UDP Communications Handler.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import socket
import Error
import Parse
import Util
from threading import Thread


class CommHandler:

    SOCKET = None
    BYTE_BUFFER_SIZE = 1024

    def __init__(self, internalIP, receivePort):
        self._internalIP = internalIP
        self._receivePort = receivePort
        self._packets = []
        try:
            self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.SOCKET.bind((self._internalIP, self._receivePort))
        except socket.error:
            # Throw "Could not initialize comms"
            Error.throw(0x0501)
        self._continue = True
        self._receiving = False

    @classmethod
    def sendAsyncPacket(cls, packet):
        _sendThread = Thread(target=packet.send)
        _sendThread.start()

    def addCyclePacket(self, packet):
        self._packets += [packet]

    def sendAll(self):
        _sendThread = Thread(target=self._sendPackets)
        _sendThread.start()

    def _sendPackets(self):
        while len(self._packets) > 0:
            self._packets[0].send()
            if len(self._packets) > 0:
                del self._packets[0]

    def stopComms(self):
        self._continue = False

    def getReceivingStatus(self):
        return self._receiving

    # Meant to be threaded on system
    # Otherwise there will be an infinite loop
    def receiveMessagesOnThread(self):
        self._continue = True
        try:
            while self._continue:
                self.SOCKET.listen(1)
                client, clientAddr = self.SOCKET.accept()
                self._receiving = True
                data = client.recv(self.BYTE_BUFFER_SIZE)
                self._receiving = False
                Parse.queueMessage(Message(data, clientAddr))
        except socket.error:
            # Throw "Failed to begin receive process"
            Error.throw(0x0502)
        except:
            # Throw "Could not initialize comms"
            Error.throw(0x0501)


class Message:

    def __init__(self, data, fromAddr):
        self.data = Util.chartobytes(data)
        self.ID = int(self.data[33:40])
        self.fromAddr = fromAddr
