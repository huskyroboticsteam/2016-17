import Adafruit_BBIO.PWM as PWM

class Servo_Sweep(object):

    def __init__(self):
        self.servo_pin = "P8_13"
        self.duty_min = 3
        duty_max = 14.5
        duty_span = self.duty_max - self.duty_min

        PWM.start(self.servo_pin, (100 - self.duty_min), 60.0, 1)
        self.left = 120
        self.center = 90
        self.right = 60
        self.clockwise = False
        self.currentAngle = 90

    def move(self):
        # first checks to see if the servo has reached the ends and reverses
        if self.currentAngle >= self.left:
            self.clockwise = True
        elif self.currentAngle <= self.right:
            self.clockwise = False
        # move the servo
        if self.clockwise:
            angle = self.currentAngle - 1
        else:
            angle = self.currentAngle + 1
        angle_f = float(angle)
        duty = 100 - ((angle_f / 180) * self.duty_span + self.duty_min)
        PWM.set_duty_cycle(self.servo_pin, duty)

def main ():
    runner = Servo_Sweep()
    while True:
        runner.move()

if __name__ == "__main__":
    main()
