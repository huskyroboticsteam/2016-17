"""
Packet Handler wrapper.

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
Questions/Comments? Email: jadenjb@uw.edu
(Untested as of 2/6/2017)

"""
import socket


class Packet:

    def __init__(self, targetIP, targetPort):
        self._data = 0
        self._targetIP = targetIP
        self._targetPort = targetPort

    # Append bitwise list to current packet buffer
    # EG [0,1,1,0]
    def appendData(self, data):
        self._data += data

    # Clear buffer
    def clear(self):
        self._data = 0

    # Sends data to constructor-specified client
    def send(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(self._data, self._targetIP)
        s.close()
