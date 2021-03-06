import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import Servo_Sweep
import Sonar
import Navigation
import Utils

# This class is used for testing purposes only
# It tests the servos and sonar for the scanner

class Scan_Tester:
    def __init__(self):
        self.rotatorh = Servo_Sweep.Servo_Sweep(0.3, 1, 179, "P8_13", 1.125)
#        self.rotatorv = Servo_Sweep.Servo_Sweep(0.3, 70, 90, "P8_19", 0)
        self.scanner = Sonar.Sonar("AIN6")
#        self.nav = Navigation.Navigation(0.765555, 0.552777, 0.348333, 0.001, "AIN2")

    def run (self):
        self.rotatorh.move()
#        self.rotatorv.move()
        angle = self.rotatorh.getAngle()
        distance = self.scanner.readDisInch()

        print "angle: " + str(angle)
        print"distance: " + str(distance)

    def move(self):
        self.rotatorh.move()
#        self.rotatorv.move()

    def getVals(self):
        angle = self.rotatorh.getAngle()
        distance = self.scanner.readDisInch()
#        distanceReal = self.scanner.readTrueDisInch(self.rotatorv.getAngle()-90) # Might need to change this depending on servo position
        roverAngle = 90 - angle
#        realAngle = roverAngle + self.nav.getMag()
#        if(realAngle < 0 ):
#            realAngle = realAngle + 360
#        if(realAngle > 360):
#            realAngle = realAngle - 360


        print "Rover angle: " + str(roverAngle)
#        print "Real angle: " + str(realAngle)
        print "Raw Distance to obstacle: " + str(distance) + " inches (" + str(distance * 0.0254) + " meters) "
        print "Psuedo gps: " + str(Utils.getNewGPS((0,0), Utils.normalize_angle(roverAngle), distance * 0.0254))
#        print "Adjusted Distance to obstacle: " + str(distanceReal) + " inches"

    def getDis(self):
        return self.scanner.readDisInch()

    def stop(self):
        self.rotater.stop()


def main():
    runner = Scan_Tester()

    choice = raw_input('Chose test mode \n 0 for continuous read \n 1 For obstacle read')

    if choice == "0":
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

    else:
        while True:
            looping = True
            print "Scanning ..... "
            count = 0
            while looping:
                runner.move()
                if (runner.getDis() < 150): # TODO: Made this if statement distance a global variable
                    if count > 5:
                        looping = False
                    else:
                        count+= 1
                else:
                    count = 0
            print "Obstacle Detected! "
            runner.getVals()
            choice = raw_input('Press any key to continue')




if __name__ == "__main__":
    main()
