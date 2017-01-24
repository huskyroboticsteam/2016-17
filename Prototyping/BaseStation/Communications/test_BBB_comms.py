import socket
import struct
import time

throttle = -421
steering = 280
format_string = "<hh"
timeLastSend = time.time()

RCV_IP = "192.168.1.40"
RCV_PORT = 8888

SND_IP = "192.168.7.2"
SND_PORT = 8887

MESSAGE = struct.pack(format_string, throttle, steering)

print "UDP target IP:", SND_IP
print "UDP target port:", SND_PORT

rcv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcv_sock.bind((RCV_IP, RCV_PORT))
snd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send():
    global timeLastSend
    if (time.time() - timeLastSend > 1000):
        print "message:", MESSAGE
        snd_sock.sendto(MESSAGE, (SND_IP, SND_PORT))
        timeLastSend = time.time()


def receive():
    print("attempt receive")
    data, addr = rcv_sock.recvfrom(1024)  # buffer size is 1024 bytes
    rcv_throttle, rcv_steering = struct.unpack(format_string, data)
    print("received message:", rcv_throttle, rcv_steering)


while True:
    send()
    receive()
