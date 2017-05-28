import Adafruit_BBIO.PWM as PWM

'''
Used to move the servo
Servo value of 180 is to the far left
Servo value of 0 is to the far right
Note: Depending on servo, 90 may not be center

Used by:
    Robot.py
    RobotTest.py
    Scan_Tester.py

'''
class Servo_Sweep(object):

    def __init__(self, speed, min, max, pin, offset):
        '''
        Args:
            speed: float of servo speed. Higher values will move servo faster
            min: An int representing the right limit of sweeping the servo. 1 Will be full right
            max: An int representing the left limit of sweeping the servo. 179 will be full left
            pin: A string for the analog pin name
            offset: The amount to shift for the internal servo values and actual heading

        '''
        self.servo_pin = pin
        self.duty_min = 3
        self.duty_max = 14.5
        self.duty_span = self.duty_max - self.duty_min
        self.turn_speed = speed
        PWM.start(self.servo_pin, (100 - self.duty_min), 60.0, 1)
        self.left = max
        self.right = min
        self.center = (max + min) / 2
        self.clockwise = False
        self.currentAngle = 90.0
        self.pin = pin
        self.offset = offset

    # Moves the servo back and forth
    def move(self):
        # first checks to see if the servo has reached the ends and reverses
        if self.currentAngle >= self.left:
            self.clockwise = True
        elif self.currentAngle <= self.right:
            self.clockwise = False
        # move the servo
        if self.clockwise:
            self.currentAngle = self.currentAngle - self.turn_speed
        else:
            self.currentAngle = self.currentAngle + self.turn_speed
        angle_f = float(self.currentAngle)
        duty = 100 - ((self.currentAngle / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

    def getAngle(self):
        return self.currentAngle + self.offset

    def stop(self):
        PWM.stop(self.pin)
        PWM.cleanup()


def main():
    runner = Servo_Sweep(0.2, 1, 179, "P8_13")
    choice = raw_input('Chose test mode \n 0 for auto servo move \n 1 for manual servo move')
    if choice == "0":
        while True:
            runner.move()
    else:
        while True:
            angle = raw_input("Angle (0 to 180 x to exit):")
            if angle == 'x':
                PWM.stop(servo_pin)
                PWM.cleanup()
                break
            angle_f = float(angle)
            duty = 100 - ((angle_f / 180) * duty_span + duty_min)
            PWM.set_duty_cycle(servo_pin, duty)



if __name__ == "__main__":
    main()
