class Motor:
    """ Controls a single motor. """

    def __init__(self, motor_id):
        """
        motor_id is an arbitrary number to identify motors
        """
        self.motor_id = motor_id
        # Constant for how much motor power can change from one time step to another.
        self.MAX_MOTOR_VAL_DIFF = 10


    def set_motor(self, motor_val):
        """
        Make motor turn with power as near as possible to `motor_val`, but
        don't change motor speed to abruptly
        Use negative values to go backwards.
        """
        pass

    def set_motor_exactly(self, motor_val):
        """
        Make motor turn with power exactly `motor_val`, without any safety checks.
        Use negative values to go backwards.
        Internal use only.
        """
        pass
