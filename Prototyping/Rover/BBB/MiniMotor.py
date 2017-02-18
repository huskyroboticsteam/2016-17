import Motor.py
import Adafruit_PCS9685
# Constant for how much motor power can change from one time step to another.



class MiniMotor(Motor):
    """ Controls a single motor. """

    def __init__(self, motor_id, throttle_pin, forward_pin, back_pin, pwm):
        """
        motor_id is an arbitrary number to identify motors
        throttle_pin, forward_pin, and back_pin should be the relevant pin IDs. (int)
        pwm should be created by Adafruit_PCA9685.PCA9685(...)
        """
        super(motor_id)
        self.throttle_pin = throttle_pin
        self.forward_pin = forward_pin
        self.back_pin = back_pin
        self.pwm = pwm
        self.set_motor_exactly(0)
        self.prev_motor_val = 0

    def set_motor(self, motor_val):
        """
        Make motor turn with power as near as possible to `motor_val`, but
        don't change motor speed to abruptly
        Use negative values to go backwards.
        """
        motor_val = int(motor_val)
        if abs(motor_val) > 255:
            print "bad value for motor_val in set_motor: " + str(motor_val)
            return
        diff = motor_val - self.prev_motor_val
        diff = max(-self.MAX_MOTOR_VAL_DIFF, min(self.MAX_MOTOR_VAL_DIFF, diff))  # clamp value into range
        actual_motor_val = self.prev_motor_val + diff
        self.prev_motor_val = actual_motor_val
        print "trying to drive motor: " + str(self.motor_id) + " with value: " + str(motor_val) \
              + ", actual value: " + str(actual_motor_val)
        self.set_motor_exactly(actual_motor_val)

    def set_motor_exactly(self, motor_val):
        """
        Make motor turn with power exactly `motor_val`, without any safety checks.
        Use negative values to go backwards.
        Internal use only.
        """
        self.pwm.set_pwm(self.forward_pin, 4096, 0)
        self.pwm.set_pwm(self.back_pin, 4096, 0)
        self.pwm.set_pwm(self.throttle_pin, 2048 - abs(motor_val) * 8, 2048 + abs(motor_val) * 8)
        if motor_val > 0:
            self.pwm.set_pwm(self.forward_pin, 0, 4096)
        else:
            self.pwm.set_pwm(self.back_pin, 0, 4096)
