import socket
from struct import *

class UDP:
    def __init__(self, IP, PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))
        self.format = "ff?"
        
    def read(self):
        packet = (unpack(self.format, self.sock.recv(64)))
        return packet
    