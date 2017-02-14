import socket
import struct
UDP_IP = "192.168.0.40"
print(UDP_IP)
UDP_PORT = 8888
format_string = "<hh"
    
sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
    
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    throttle, steering = struct.unpack(format_string, data)
    print("received message:", throttle, steering)
