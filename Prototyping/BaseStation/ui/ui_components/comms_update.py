from PyQt4 import QtCore
import socket, struct
from Queue import Queue


class CommsUpdate:

    ROVER_HOST = "12.12.12.12";
    ROVER_PORT = 1234;

    def __init__(self, command):

        self.command_api = command

        # self.rover_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.rover_sock.connect((self.ROVER_HOST, self.ROVER_PORT))
        # self.rover_sock.setblocking(False)

        # timer = QtCore.QTimer()
        # timer.connect(self.send_message)
        # timer.connect(self.recieve_message)
        # timer.start()

    def send_message(self):

        # Put the first 2 boolean values in the buffer
        buff = struct.pack("<??", True, auto_flag)
        # Put the next 2 short values in the buffer
        struct.pack("<hh", buff, 2, joystick_accel, joystick_rotate)

        # self.rover_sock.send(buff)

        # TODO: Add sending code for the arm

    def send_auto_mode(self, lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec):

        # Put the first boolean value in the buffer
        buff = struct.pack("<?", False)
        # Put the next 6 shorts in the buffer
        buff = struct.pack("<hhhhhhh", buff, 1, lat_deg, lat_min, lat_sec, lng_deg, lng_min, lng_sec)

        self.rover_sock.send(buff)

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
