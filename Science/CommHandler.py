"""
UDP Communications Handler.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import socket
import sys
from threading import Thread


class CommHandler:

    SOCKET = None
    BYTE_BUFFER_SIZE = 1024
    TCP_SEND_TIMEOUT = 300

    def __init__(self, internalIP, receivePort):
        self._internalIP = internalIP
        self._receivePort = receivePort
        self._packets = []
        self.SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SOCKET.bind((self._internalIP, self._receivePort))
        self._messages = []
        self._continue = True
        self._receiving = False


    def addCyclePacket(self, packet):
        self._packets += [packet]

    def sendAll(self):
        _sendThread = Thread(target=self._sendPackets)
        _sendThread.start()

    def _sendPackets(self):
        sys.stdout.write("Len: " + str(len(self._packets)) + "\n")
        while len(self._packets) > 0:
            self._packets[0].send()
            del self._packets[0]

    def resetPackets(self):
        self._packets = []

    def waitingPackets(self):
        return len(self._packets) >= 1

    def viewPackets(self):
        return self._packets

    def waitingMessages(self):
        return len(self._messages) >= 1

    # Returns and deletes messages
    def getMessages(self):
        temp = self._messages
        self._messages = []
        return temp

    def viewMessages(self):
        return self._messages

    def stopComms(self):
        self._continue = False

    def getReceivingStatus(self):
        return self._receiving

    # Meant to be threaded externally
    # Otherwise there will be an infinite loop
    def receiveMessagesOnThread(self):
        self._continue = True
        try:
            while self._continue:
                self.SOCKET.listen(1)
                client, clientAddr = self.SOCKET.accept()
                self._receiving = True
                data = client.recv(self.BYTE_BUFFER_SIZE)
                self._messages += [Message(data, clientAddr)]
        except socket.error:
            pass
        self._receiving = False


class Message:

    def __init__(self, data, fromAddr):
        self.DATA = data
        self.fromAddr = fromAddr
