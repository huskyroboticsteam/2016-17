from recUDP import *
from struct import *
from motor import *

from bbio import *

class Control:
    def __ini__(self):
        pass
    def UDP_start(self):
        self.UDP = UDP("192.168.1.80", 8888)

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
bbio_cleanup()