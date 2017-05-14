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
    BYTE_BUFFER_SIZE = 2048

    def __init__(self, internalIP, receivePort):
        CommHandler._internalIP = internalIP
        CommHandler._receivePort = receivePort
        CommHandler._packets = []
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
        cls.sendAll()

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
                client.close()
        except socket.error:
            # Throw "Failed to begin receive process"
            Error.throw(0x0502)
        except:
            sys.stderr.write("\nUnexpected error: " + str(sys.exc_info()[0]) + "\n")
            # Throw "Could not initialize comms"
            Error.throw(0x0501)
    
    @classmethod
    def addCyclePacket(cls, packet):
        cls._packets += [packet]
        #Util.write(len(cls._packets))

    @classmethod
    def sendAll(cls):
        _sendThread = Thread(target=cls._sendPackets)
        _sendThread.start()

    @classmethod
    def _sendPackets(cls):
        while CommHandler._continue:
            Util.write(len(cls._packets))
            if len(cls._packets) > 0:
                cls._packets.pop(0).send()
    
    @classmethod
    def stopComms(cls):
        CommHandler._continue = False


class Message:

    def __init__(self, data, fromAddr):
        self.data = bytearray(data) 
        self.ID = self.data[4]
        self.fromAddr = fromAddr

    def __str__(self):
        return "\nID: " + hex(self.ID) + "\tData:" + str(self.data) + "\n"
