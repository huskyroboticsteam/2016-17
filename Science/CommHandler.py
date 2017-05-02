"""
TCP/UDP Communications Handler.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import sys
import socket
import Error
import Parse
import Util
from threading import Thread


class CommHandler:

    SOCKET = None
    BYTE_BUFFER_SIZE = 1024

    def __init__(self, internalIP, receivePort):
        CommHandler._internalIP = internalIP
        CommHandler._receivePort = receivePort
        self._packets = []
        try:
            CommHandler.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            CommHandler.SOCKET.bind((CommHandler._internalIP, CommHandler._receivePort))
        except socket.error:
            # Throw "Could not initialize comms"
            Error.throw(0x0501)
        CommHandler._continue = True
        CommHandler._receiving = False

    @classmethod
    def startCommsThread(cls):
        comms_thread = Thread(target=cls.receiveMessagesOnThread)
        comms_thread.start()

    @classmethod
    def sendAsyncPacket(cls, packet):
        _sendThread = Thread(target=packet.send)
        _sendThread.start()

    # Meant to be threaded on system
    # Otherwise there will be an infinite loop
    @classmethod
    def receiveMessagesOnThread(cls):
        CommHandler._continue = True
        try:
            while CommHandler._continue:
                CommHandler.SOCKET.listen(1)
                client, clientAddr = CommHandler.SOCKET.accept()
                CommHandler._receiving = True
                data = client.recv(CommHandler.BYTE_BUFFER_SIZE)
                if not data:
                    break
                CommHandler._receiving = False
                Parse.queueMessage(Message(data, clientAddr))
                sys.stdout.write("\nMessage received: " + str(data) + "\n")
                client.close()
        except socket.error:
            # Throw "Failed to begin receive process"
            Error.throw(0x0502)
        except:
            sys.stderr.write("\nUnexpected error: " + str(sys.exc_info()[0]) + "\n")
            # Throw "Could not initialize comms"
            Error.throw(0x0501)

    def addCyclePacket(self, packet):
        self._packets += [packet]

    def sendAll(self):
        _sendThread = Thread(target=self._sendPackets)
        _sendThread.start()

    def _sendPackets(self):
        while len(self._packets) >= 1:
            self._packets[0].send()
            if len(self._packets) >= 1:
                del self._packets[0]

    def stopComms(self):
        CommHandler._continue = False


class Message:

    def __init__(self, data, fromAddr):
        self.data = Util.chartobytes(data)
        self.ID = int(self.data[32:40], 2)
        self.fromAddr = fromAddr

