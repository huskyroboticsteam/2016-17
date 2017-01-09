import socket
from struct import *

class UDP:
    def __init__(self, IP, PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))
        #use socket from python, needs (import socket)
        self.format = "ff?"
        #format for struct

    #takes the udp packet from the sending computer then returns packet
    def read(self):
        packet = (unpack(self.format, self.sock.recv(64)))
        return packet
