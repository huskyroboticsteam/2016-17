__author__ = 'Trevor'

import socket
import threading
import pygame
from GPSCoordinates import *

class receiveOverUDP(threading.Thread):
    def __init__(self, ownIP, udpPort):
        threading.Thread.__init__(self)
        self.OwnIP = ownIP
        self.UDPPort = udpPort
        self.sockCome = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.on = True
        try:
            self.sockCome.bind((self.OwnIP, self.UDPPort))
        except socket.error:
            self.on = False
            print "Error connecting to rover."
        self.End = False # Make True to end receiving thread
        self.Coord = [0,0]
        self.Potentiometer = 0
        self.Magnetometer = 0
        #self.sockCome.settimeout(0.01)

        #DEBUG:
        self.addr = 0

    def run(self):
        while not self.End:
            if self.on == True:
                data, addr = self.sockCome.recvfrom(1024)
                self.addr = addr

                if self.addr[0] == '192.168.1.52':
                    dataArray = data.split(',')
                    LatitudeChars = list(dataArray[0])
                    LatitudeDegrees = LatitudeChars[0] + LatitudeChars[1]
                    LatitudeMinutes = LatitudeChars[2] + LatitudeChars[3] + LatitudeChars[4] + LatitudeChars[5] + LatitudeChars[6] + LatitudeChars[7] + LatitudeChars[8]
                    LatitudeString = LatitudeDegrees + '*' + LatitudeMinutes

                    LongitudeChars = list(dataArray[1])
                    LongitudeDegrees = LongitudeChars[0] + LongitudeChars[1] + LongitudeChars[2]
                    LongitudeMinutes = LongitudeChars[3] + LongitudeChars[4] + LongitudeChars[5] + LongitudeChars[6] + LongitudeChars[7] + LongitudeChars[8] + LongitudeChars[9]
                    LongitudeString = '-' + LongitudeDegrees + '*' + LongitudeMinutes
                    CoordinateString = LatitudeString + ',' + LongitudeString
                    DecimalCoord = Coordinates(CoordinateString)

                    print self.Coord[0]
                    print self.Coord[1]

                    self.Coord[0] = DecimalCoord.latitude
                    self.Coord[1] = DecimalCoord.longitude

                elif self.addr[0] == '192.168.1.51':
                    dataArray = data.split(',')
                    self.Magnetometer = dataArray[0]
                    self.Potentiometer = dataArray[1] # 2 or 3?

                elif self.addr[0] == '192.168.1.7':
                    print data
                    print "first byte: " + str(int(data[0]))
                    print "second byte: " + str(int(data[1]))

            # print data
            #
            # dataArray = data.split(',')
            # LatitudeChars = list(dataArray[0])
            # LatitudeDegrees = LatitudeChars[0] + LatitudeChars[1]
            # LatitudeMinutes = LatitudeChars[2] + LatitudeChars[3] + LatitudeChars[4] + LatitudeChars[5] + LatitudeChars[6] + LatitudeChars[7] + LatitudeChars[8]
            # LatitudeString = LatitudeDegrees + '*' + LatitudeMinutes
            #
            # LongitudeChars = list(dataArray[1])
            # LongitudeDegrees = LongitudeChars[0] + LongitudeChars[1] + LongitudeChars[2]
            # LongitudeMinutes = LongitudeChars[3] + LongitudeChars[4] + LongitudeChars[5] + LongitudeChars[6] + LongitudeChars[7] + LongitudeChars[8] + LongitudeChars[9]
            # LongitudeString = '-' + LongitudeDegrees + '*' + LongitudeMinutes
            # CoordinateString = LatitudeString + ',' + LongitudeString
            # DecimalCoord = Coordinates(CoordinateString)
            #
            # self.Coord[0] = DecimalCoord.latitude
            # self.Coord[1] = DecimalCoord.longitude
            #
            # # TO ADD:
            # self.Potentiometer = dataArray[2] # 2 or 3?
            # self.Magnetometer = dataArray[3]

            #DEBUG:
            #self.Coord = (47.653870,-122.307833)
            #self.Magnetometer = self.Magnetometer + .001
            #self.Latitude = dataStrings[0]
