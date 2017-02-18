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

UDP_IP = "192.168.0.60"
UDP_PORT = 58152

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)

while True:
    line = "1 1"
    if len(line.split(" ")) == 2:
        throttle = line.split(" ")[0]
        steering = line.split(" ")[1]
        MESSAGE = struct.pack(format_string, drive_flag, auto, int(throttle), int(steering))
        print "sent message:", MESSAGE
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    try:
        data = sock.recv(1024)
        MESSAGE = struct.unpack("<fffffhhhhhh", data)
        print "received message:", MESSAGE
    except: #ValueError as e:
        #if e.message == 'Caught an exception while rendering: too many values to unpack':
        pass
    time.sleep(2)
