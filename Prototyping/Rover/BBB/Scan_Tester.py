import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import Servo_Sweep
import Sonar

class Scan_Tester:
    def __init__(self):
        self.rotater = Servo_Sweep.Servo_Sweep()
        self.scanner = Sonar.Sonar()

    def run (self):
        self.rotater.move()
        angle = self.rotater.getSonarHeading()
        distance = self.scanner.readDisKm()
        print "angle: " + str(angle)
        print"distance: " + str(distance)

def main():
    runner = Scan_Tester()
    while True:
        runner.run()


if __name__ == "__main__":
    main()
