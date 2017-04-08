import Motor
import Adafruit_BBIO.PWM as PWM
import Utils

class BigMotor(Motor.Motor):

    def __init__(self, motor_id, pin):
        super(BigMotor, self).__init__(motor_id)
        try:
            self.pin = pin
            PWM.start(self.pin, 150/17.6, 60)
            self.set_motor_exactly(0)
        except:
            print("motor: " + str(motor_id) + " disconnected")

    def set_motor_exactly(self, motor_val):
        if self.prev_motor_val > 0 and motor_val < 0:
            print("breaking")
            motor_val = 0
        try:
            motor_val = int(motor_val)
            if abs(motor_val) > 255:
                print "bad value for motor_val in set_motor_exatly: " + str(motor_val)
            PWM.set_duty_cycle(self.pin, Utils.translateValue(motor_val, -255, 255, 100/17.6, 200/17.6))
            self.prev_motor_val = motor_val
        except:
            print("motor: " + str(self.motor_id) + " disconnected")
            print motor_val
            print self.pin