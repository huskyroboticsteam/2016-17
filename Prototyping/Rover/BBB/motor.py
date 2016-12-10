from bbio import *
from bbio.libraries.Servo import *
#use the following to change bbio's servo class
#Servo(pwm_pin=None, pwm_freq=50, min_ms=0.5, max_ms=2.4)

class motor:
    def __init__(self, m_pin):
        self.servo = Servo()
        self.servo.attach(m_pin)
        self.servo.write(90)
        
    def drive(self, value):
        value = self.convert(value, -1, 1, 0, 180)
        self.servo.write(value)
        #.write controls servo, ranges from 0 to 180
        #90 is neutral

    #converts a number from one range to another
    def convert(self, value, r_min, r_max, d_min, d_max):
        r_range = r_max - r_min
        d_range = d_max - d_min
        scale = float(r_max - value) / r_range
        return r_min + (scale * d_range)
