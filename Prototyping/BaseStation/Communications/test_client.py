#!/usr/bin/env python

import socket
import struct
import time
import fileinput

drive_flag = True
auto = False
throttle = 20
steering = 10
format_string = "<??hh"

UDP_IP = "192.168.0.40"
UDP_PORT = 8840


print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    for line in fileinput.input():
        if len(line.split(" ")) == 2:
            throttle = line.split(" ")[0]
            steering = line.split(" ")[1]
            MESSAGE = struct.pack(format_string, drive_flag, auto, int(throttle), int(steering))
            print "message:", MESSAGE
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
