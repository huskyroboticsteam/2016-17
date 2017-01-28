from recUDP import *
from struct import *
from motor import *
from bbio import *

FRONT_RIGHT = 1
FRONT_LEFT = 2

motorrs[FRONT_RIHGT]

class Control:
    def __ini__(self):
        pass

    #make a udp connection
    #use ip of the receiving computer, be wary of port
    #UDP(IP, PORT)
    def UDP_start(self):
        self.UDP = UDP("192.168.1.80", 8888)

    #takes packet and assigns variables from the packet
    def UDP_get(self):
        packet = self.UDP.read()
        self.throttle, self.turn, self.auto = packet
        '''print throttle
        print turn
        print auto'''

    def main(self):
        self.UDP_start()
        self.FLmotor = motor(PWM1A)
        while(1):
            try:
                self.UDP_get()
                self.FLmotor.drive(self.throttle)
            except KeyboardInterrupt:
                break

app = Control()
app.main()
print "exit ok"
#bbio_cleanup()
#you want a cleanup phrase before code ends