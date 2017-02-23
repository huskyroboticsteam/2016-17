from PyQt4 import QtCore
import socket, struct
from Queue import Queue
import random


class CommsUpdate:

    ROVER_HOST = "192.168.0.40"
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

            # TCP connection to the rover
            self.auto_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.auto_sock.setblocking(False)
            self.auto_sock.connect((self.ROVER_HOST, self.ROVER_TCP_PORT))
        except socket.error():
            print "Can't connect to rover"

        # Do this code if there was no exception in connecting
        else:
            self.timer = QtCore.QTimer()
            # self.timer.timeout.connect(self.send_message)
            # self.timer.timeout.connect(self.receive_message)
            self.timer.start(500)

    def shutdown(self):
        self.auto_sock.close()
        self.rover_sock.close()

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
        rover_data = self.rover_sock.recv(1024)

        # Unpack the first six floats of the packet
        tup = struct.unpack_from("<ffffff", rover_data, 0)
        pot = tup[0]
        mag = tup[1]
        enc_1 = tup[2]
        enc_2 = tup[3]
        enc_3 = tup[4]
        enc_4 = tup[5]

        # Unpack the next six shorts of the packet (should reach the end of the rover packet)
        tup = struct.unpack_from("<hhhhhh", rover_data, 0)
        lat_deg = tup[0]
        lat_min = tup[1]
        lat_sec = tup[2]
        lng_deg = tup[3]
        lng_min = tup[4]
        lng_sec = tup[5]

        self.command_api.update_sensors(pot, mag, enc_1, enc_2, enc_3, enc_4)
        self.command_api.update_rover_pos(lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec)

        # TODO: add arm packets structure
