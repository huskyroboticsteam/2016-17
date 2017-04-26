import socket
import struct
import threading
import time

class Robot_comms():

    def __init__(self, robot_ip, udp_port, tcp_port, d_format, gps_format, rtb_format, aut_format):
        self.receivedDrive = None
        self.robot_ip = robot_ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.base_station_ip = None
        self.driveFormat = d_format
        self.gpsFormat = gps_format
        self.rtbFormat = rtb_format
        self.aut_format = aut_format
        self.udp_sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.udp_sock.bind((self.robot_ip, self.udp_port))
        self.udp_sock.setblocking(False)

        self.tcp_sock = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_STREAM) # TCP
        self.tcp_sock.bind((self.robot_ip, self.tcp_port))
        self.tcp_sock.setblocking(False)
        self.tcp_sock.listen(1)
        self.conn = None
        self.lat = 0
        self.longitude = 0
        self.nav = None
        self.most_recent_packet = None
        # Starts gps looping and updating every second
        self.updateGPS()

    # Attempts to update the GPS coords every second. Only should work every 2 seconds
    # since gps only sends the correct message 50% of the time. If there is latency,
    # it is because the GPS is being updated too frequently.
    def updateGPS(self):
        try:
            gps = self.nav.getGPS()
            if gps is not None:
                self.lat = float(gps[0])
                self.longitude = float(gps[1])
        except:
            pass
        # Currently set to 1 second
        threading.Timer(1, self.updateGPS).start()

    # receives a packet and sets variables accordingly
    def receiveData(self, nav):
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
                    drive_unpacked = struct.unpack(self.driveFormat, data)
                    self.receivedDrive = drive_unpacked
                    hasRecieved = False
                # If one second has elapsed since the last packet received, stop
                if time.time() - self.most_recent_packet == 1:
                    self.receivedDrive = None

        except socket.error:
            # TODO: catch exceptions from the non-blocking receive better
            pass
        try:
            if self.conn is None:
                self.conn, tcp_addr = self.tcp_sock.accept()
                self.conn.setblocking(False)
                self.base_station_ip = tcp_addr
            data = self.conn.recv(1024)
            gps_unpacked = struct.unpack(self.gpsFormat, data)
            if gps_unpacked[0]:
                nav.append_destination(gps_unpacked[1:])
            else:
                self.closeConn()
        except socket.error:
            # TODO: catch exceptions better
            pass

    # sends data in message back to the base station
    def sendData(self, nav):
        self.nav = nav
        try:
            # Only sends once it has received at least one message
            if self.base_station_ip is not None:
                # Follows format: potentiometer, magnetometer, encoders 1-4, latitude, longitude
                MESSAGE = struct.pack(self.rtbFormat, nav.readPot(), nav.getMag(), 0, 0, 0, 0, self.lat, self.longitude)
                self.udp_sock.sendto(MESSAGE, self.base_station_ip)
        except socket.error:
            pass

    # sends true, lat, long, true to base station, indicating that the robot is at the desired position
    def sendAtLocationPacket(self, nav):
        self.nav = nav
        try:
            if self.base_station_ip is not None:
                # Follows format: true, lat, long, true
                MESSAGE = struct.pack(self.aut_format, True, self.lat, self.longitude, True)
                self.udp_sock.sendto(MESSAGE, self.base_station_ip)
        except socket.error:
            pass

    def closeConn(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
