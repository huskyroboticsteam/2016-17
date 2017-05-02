import Adafruit_BBIO.PWM as PWM

class Servo_Sweep(object):

    def __init__(self):
        self.servo_pin = "P8_13"
        self.duty_min = 3
        self.duty_max = 14.5
        self.duty_span = self.duty_max - self.duty_min

        PWM.start(self.servo_pin, (100 - self.duty_min), 60.0, 1)
        self.left = 179
        self.center = 90
        self.right = 1
        self.clockwise = False
        self.currentAngle = 90.0

    def move(self):
        # first checks to see if the servo has reached the ends and reverses
        if self.currentAngle >= self.left:
            self.clockwise = True
        elif self.currentAngle <= self.right:
            self.clockwise = False
        # move the servo
        if self.clockwise:
            self.currentAngle = self.currentAngle - 0.005
        else:
            self.currentAngle = self.currentAngle + 0.005
        angle_f = float(self.currentAngle)
        duty = 100 - ((self.currentAngle / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

def main ():
    runner = Servo_Sweep()
    while True:
        runner.move()

if __name__ == "__main__":
    main()
