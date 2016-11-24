#!/usr/bin/env python

import socket
import struct
import time

throttle = -421
steering = 280
format_string = "<hh"

UDP_IP = "192.168.1.40"
UDP_PORT = 8888
MESSAGE = struct.pack(format_string, throttle, steering)

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    print "message:", MESSAGE
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(1)
