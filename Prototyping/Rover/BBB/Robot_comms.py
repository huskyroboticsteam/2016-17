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
            unpacked = struct.unpack(self.driveFormat, data)
            self.receivedDrive = unpacked
            print "drive received"
            print unpacked

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
            unpacked = struct.unpack(self.gpsFormat, data)
            if unpacked[0]:
                nav.append_destination(unpacked[1:])
                print "gps received"
                print unpacked
            else:
                self.closeConn()
        except:
            # TODO: catch exceptions better
            pass

    # sends data in message back to the base station
    def sendData(self, nav):
        pass
        # TODO: do this
        # read data from sensors or read class variables

    def closeConn(self):
        if self.conn != None:
            self.conn.close()
            self.conn = None
