__author__ = 'Trevor'

import socket

class sendOverUDP:
    def __init__(self, targetIP, udpPort):
        self.TargetIP = targetIP
        self.UDPPort = udpPort
        self.sockBalls = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sockBalls.settimeout(0.01)

    def sendItOff(self, messageUDP):
        #print str(messageUDP)
        self.sockBalls.sendto(messageUDP, (self.TargetIP, self.UDPPort))
        print messageUDP + " " + self.TargetIP