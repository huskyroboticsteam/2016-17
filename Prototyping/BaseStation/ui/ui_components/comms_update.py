from PyQt4 import QtCore
import socket, struct
import random


class CommsUpdate:

    ROVER_HOST = "192.168.0.40"
    LOCAL_HOST = "127.0.0.1"
    ROVER_PORT = 8840

    ROVER_TCP_PORT = 8841

    def __init__(self, command):

        # Indicates whether the rovers is in autonomous mode
        self.auto = False

        self.command_api = command

        try:
            # UDP connection to the rover
            self.rover_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.rover_sock.setblocking(False)

        except socket.error():
            print "Can't connect to rover"

        # Do this code if there was no exception in connecting
        else:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.send_message)
            self.timer.timeout.connect(self.receive_message)
            self.timer.start(500)

    def shutdown(self):
        self.rover_sock.close()

    def open_tcp(self):
       # TCP connection to the rover
        self.auto_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.auto_sock.connect((self.ROVER_HOST, self.ROVER_TCP_PORT))

    def close_tcp(self):
        self.auto_sock.close()

    def send_message(self):

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<?hh", self.auto, random.randint(-255, 255), random.randint(-100, 100))

        self.rover_sock.sendto(buff, (self.ROVER_HOST, self.ROVER_PORT))

        # TODO: Add sending code for the arm

    def send_auto_mode(self, more, lat, lng):

        # Put the first boolean value in the buffer
        buff = struct.pack("<?ff", more, lat, lng)

        self.auto_sock.send(buff)

    def receive_message(self):

        try:
            rover_data = self.rover_sock.recv(1024)
        except:
            print
        else:
            # Unpack the first six floats of the packet
            tup = struct.unpack_from("<ffffffff", rover_data, 0)
            pot = tup[0]
            mag = tup[1]
            enc_1 = tup[2]
            enc_2 = tup[3]
            enc_3 = tup[4]
            enc_4 = tup[5]
            lat = tup[6]
            lng = tup[7]

            print str(pot) + " " + str(mag) + " " + str(lat) + " " + str(lng)

        self.command_api.update_sensors(random.randint(-255, 255), random.randint(-100, 100), 0, 0, 0, 0)
            # self.command_api.update_rover_pos(lat, lng)

            # TODO: add arm packets structure
