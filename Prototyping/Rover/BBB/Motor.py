class Motor:
    """ Controls a single motor. """

    def __init__(self, motor_id, throttle_pin, forward_pin, back_pin, pwm):
        """
        motor_id is an arbitrary number to identify motors
        throttle_pin, forward_pin, and back_pin should be the relevant pin IDs. (int)
        pwm should be created by Adafruit_PCA9685.PCA9685(...)
        """
        self.motor_id = motor_id
        self.throttle_pin = throttle_pin
        self.forward_pin = forward_pin
        self.back_pin = back_pin
        self.pwm = pwm
        self.set_motor(0)

    def set_motor(self, motor_val):
        """
        Make motor turn with power exactly `motor_val`. Use negative values to go backwards.
        """
        motor_val = int(motor_val)
        if abs(motor_val) > 255:
            print "bad value for motor_val in set_motor: " + str(motor_val)
            return
        self.pwm.set_pwm(self.forward_pin, 4096, 0)
        self.pwm.set_pwm(self.back_pin, 4096, 0)
        self.pwm.set_pwm(self.throttle_pin, 2048 - abs(motor_val) * 8, 2048 + abs(motor_val) * 8)
        if motor_val > 0:
            self.pwm.set_pwm(self.forward_pin, 0, 4096)
        else:
            self.pwm.set_pwm(self.back_pin, 0, 4096)
        print "driving motor: " + str(self.motor_id) + " with value: " + str(motor_val)
