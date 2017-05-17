import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import Servo_Sweep
import Sonar

class Scan_Tester:
    def __init__(self):
        self.rotater = Servo_Sweep.Servo_Sweep(0.5, 1, 179, "P8_13")
        self.scanner = Sonar.Sonar()

    def run (self):
        self.rotater.move()
        angle = self.rotater.getSonarHeading()
        distance = self.scanner.readDisInch()

        print "angle: " + str(angle)
        print"distance: " + str(distance)

    def getDis(self):
        print self.scanner.readDisInch()

    def stop(self):
        self.rotater.stop()

def main():
    runner = Scan_Tester()
    mode = True
    while True:
        try:
            if mode:
                runner.run()
            else:
                print runner.getDis()
        except KeyboardInterrupt:
            choice = raw_input('Press 0 to switch mode. Press 1 to continue. Anything else will exit')
            if choice[0] == '1':
                continue
            elif choice[0] == '0':
                mode = not mode
            else:
                runner.stop()
                break


if __name__ == "__main__":
    main()
