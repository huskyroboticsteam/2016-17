__author__ = 'Brian'

import socket
from time import *
from struct import *

class sendOverUDP:
    def __init__(self, targetIP, udpPort):
        self.TargetIP = targetIP
        self.UDPPort = udpPort
        self.sockBalls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #format for the packet
        self.format = "ff?"
        #self.sockBalls.settimeout(0.01)

    def get_format(self):
        return self.format

    def sendItOff(self, messageUDP):
        print str(unpack(self.format, messageUDP))
        sleep(.5)
        self.sockBalls.sendto(messageUDP, (self.TargetIP, self.UDPPort))
        print messageUDP + " " + self.TargetIP