import socket
import struct

class Robot_comms():

    def __init__(self, robot_ip, rcv_port, d_format, gps_format, rtb_format):
        self.receivedDrive = None
        self.robot_ip = robot_ip
        self.udp_port = rcv_port
        self.base_station_ip = None
        self.driveFormat = d_format
        self.gpsFormat = gps_format
        self.rtbFormat = rtb_format
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_DGRAM)  # UDP
        self.sock.bind((self.robot_ip, self.udp_port))
        self.sock.setblocking(False)

    # receives a packet and sets variables accordingly
    def receiveData(self, nav):
        try:
            data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            self.base_station_ip = addr
            unpacked = struct.unpack(self.driveFormat, data)
            if unpacked[0]:
                self.receivedDrive = unpacked[1:]
            else:
                unpacked = struct.unpack(self.gpsFormat, data)
                nav.append_destination(unpacked[1:])
            print unpacked
        except:
            # TODO: catch exceptions from the non-blocking recieve better
            pass

    # sends data in message back to the base station
    def sendData(self, nav):
        pass
        # TODO: do this
        # read data from sensors or read class variables