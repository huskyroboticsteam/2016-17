class Motor(object):
    """ Controls a single motor. """

    def __init__(self, motor_id):
        """
        motor_id is an arbitrary number to identify motors
        """
        self.motor_id = motor_id
        self.prev_motor_val = 0
        # Constant for how much motor power can change from one time step to another.
        self.MAX_MOTOR_VAL_DIFF = 100


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
        print "trying to drive motor: " + str(self.motor_id) + " with value: " + str(motor_val) \
              + ", actual value: " + str(actual_motor_val)
        self.set_motor_exactly(actual_motor_val)

    def set_motor_exactly(self, motor_val):
        """
        Make motor turn with power exactly `motor_val`, without any safety checks.
        Use negative values to go backwards.
        Should be overridden by child class.
        """
        pass
