import socket
import struct
import threading
import time

# IMPORTANT
# This code was copied from Robot_comms.py
# Please be aware that they share common functionality which should be abstracted out
# The reason this was not done is because copying code in this case is easer from an 
#   implementation standpoint at the point in the year this class was written.
# If you would like to refactor this (by introducing a Comms class), PLEASE do.
# If this note is around at the start of the 2017-2018 season or beyond, please do not
# continue work on this class until the refactorings mentioned above have been completed
# and there is less duplicated code between here and Robot_comms.py

class Arm_comms():

    def __init__(self, robot_ip, udp_port, control_format):
        self.receivedDrive = None
        self.robot_ip = robot_ip
        self.udp_port = udp_port
        #self.tcp_port = tcp_port
        self.base_station_ip = None
        self.control_format = control_format
        self.udp_sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.udp_sock.bind((self.robot_ip, self.udp_port))
        self.udp_sock.setblocking(False)

        # self.tcp_sock = socket.socket(socket.AF_INET, # Internet
        #                             socket.SOCK_STREAM) # TCP
        # self.tcp_sock.bind((self.robot_ip, self.tcp_port))
        # self.tcp_sock.setblocking(False)
        # self.tcp_sock.listen(1)
        self.conn = None
        self.most_recent_packet = time.time()

    # receives a packet and sets variables accordingly
    def receiveData(self):
        try:
            hasRecieved = False
            try:
                while True:
                    data, udp_addr = self.udp_sock.recvfrom(1024)  # buffer size is 1024 bytes
                    hasRecieved = True
                    self.most_recent_packet = time.time()
            except socket.error:
                if hasRecieved:
                    self.base_station_ip = udp_addr
                    control_unpacked = struct.unpack(self.control_format, data)
                    
                    self.receivedDrive = control_unpacked
                    hasRecieved = False
                # If one second has elapsed since the last packet received, stop
                if time.time() - self.most_recent_packet == 1:
                    self.receivedDrive = None
        except socket.error:
            # TODO: catch exceptions from the non-blocking receive better
            pass

            # Uncomment to use TCP
#        try:
#            if self.conn is None:
#                self.conn, tcp_addr = self.tcp_sock.accept()
#                self.conn.setblocking(False)
#                self.base_station_ip = tcp_addr
#            data = self.conn.recv(1024)
#            gps_unpacked = struct.unpack(self.gpsFormat, data)
#            if gps_unpacked[0]:
#                nav.append_destination(gps_unpacked[1:])
#            else:
#                self.closeConn()
#        except socket.error:
#            # TODO: catch exceptions better
#            pass

    # sends data in message back to the base station
#    def sendData(self, nav):
#        self.nav = nav
#        try:
#            # Only sends once it has received at least one message
#            if self.base_station_ip is not None:
#                # Follows format: potentiometer, magnetometer, encoders 1-4, latitude, longitude
#                MESSAGE = struct.pack(self.rtbFormat, nav.readPot(), nav.getMag(), 0, 0, 0, 0, self.lat, self.longitude)
#                self.udp_sock.sendto(MESSAGE, self.base_station_ip)
#        except socket.error:
#            pass

    def closeConn(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
