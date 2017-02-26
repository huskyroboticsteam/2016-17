import Motor
import Adafruit_BBIO.PWM as PWM
import Utils

class BigMotor(Motor.Motor):

    def __init__(self, motor_id, pin):
        super(BigMotor, self).__init__(motor_id)
        self.pin = pin
        self.last_motor_val = 0
        PWM.start(self.pin, 150/17.6, 60)
        self.set_motor_exactly(0)


    def set_motor_exactly(self, motor_val):
        motor_val = int(motor_val)
        if abs(motor_val) > 255:
            print "bad value for motor_val in set_motor_exatly: " + str(motor_val)
        PWM.set_duty_cycle(self.pin, Utils.translateValue(-255, 255, 100/17.6, 200/17.6))