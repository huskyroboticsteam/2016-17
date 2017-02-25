import socket
import struct

class Robot_comms():

    def __init__(self, robot_ip, udp_port, tcp_port, d_format, gps_format, rtb_format):
        self.receivedDrive = None
        self.robot_ip = robot_ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.base_station_ip = None
        self.driveFormat = d_format
        self.gpsFormat = gps_format
        self.rtbFormat = rtb_format
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

    # receives a packet and sets variables accordingly
    def receiveData(self, nav):
        try:
            data, udp_addr = self.udp_sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.base_station_ip = udp_addr
            drive_unpacked = struct.unpack(self.driveFormat, data)
            self.receivedDrive = drive_unpacked
            print "drive received"
            print drive_unpacked

        except:
            # TODO: catch exceptions from the non-blocking receive better
            pass
        try:
            if self.conn is None:
                print "accepting"
                self.conn, tcp_addr = self.tcp_sock.accept()
                self.conn.setblocking(False)
                print "accepted"
                self.base_station_ip = tcp_addr
            print "receiving"
            data = self.conn.recv(1024)
            print data
            print "received"
            gps_unpacked = struct.unpack(self.gpsFormat, data)
            if gps_unpacked[0]:
                nav.append_destination(gps_unpacked[1:])
                print "gps received"
                print gps_unpacked
            else:
                self.closeConn()
        except:
            # TODO: catch exceptions better
            pass

    # sends data in message back to the base station
    def sendData(self, nav):
        try:
            if self.base_station_ip is not None:
                gps = nav.getGPS()
                lat = 0
                longitude = 0
                if gps is not None:
                    lat = float(gps[0])
                    longitude = float(gps[1])
                print "sending"
                # TODO : add encoders 1-4, nav.getGPS()[3,5]
                MESSAGE = struct.pack(self.rtbFormat, nav.readPot(), nav.getMag(), 0, 0, 0, 0, lat, longitude)
                print "message packed"
                self.udp_sock.sendto(MESSAGE, self.base_station_ip)
                print "sent"
        except:
            # TODO: catch exceptions better (nav.getGPS may be null)
            pass
        # read data from sensors or read class variables

    def closeConn(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
