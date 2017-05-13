import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)

# Calculates a linear best fit for the sonar analog values
# Calibrated data is stored in SonarCalibrationData.txt
# in the form of "<slope> <intercept>"


class SonarCalibration:

    def __init__(self):
        ADC.setup()
        self.maxAnaVal = 0.8

        # X is for the analog readings
        # Y is for the distances in inches

        self.xsum = 0.0
        self.ysum = 0.0
        self.xysum = 0.0
        self.x2sum = 0.0
        self.y2sum = 0.0
        self.count = 0.0

        self.analogPin = "AIN6"

    def readAna(self): # Get raw analog value from sensor
        readVal = ADC.read("AIN6")
        print(readVal)

    def addPoint(self, distance):

        # First get the average reading from 10 analog readings
        count = 0
        total = 0.0
        while count < 10:
            readVal = ADC.read(self.analogPin)
            total += readVal
            count += 1
        analogVal = total / 10.0

        # Add to totals
        self.xsum += analogVal
        self.ysum += distance
        self.xysum += analogVal * distance
        self.x2sum += analogVal * analogVal
        self.y2sum += distance * distance
        self.count += 1

    def getSlope(self):
        return ((self.count * self.xysum) - (self.xsum * self.ysum)) / ((self.count * self.x2sum) - (self.xsum * self.xsum))

    def getIntersept(self):
        return ((self.x2sum * self.ysum) - (self.xsum * self.xysum)) / ((self.count * self.x2sum) - (self.xsum * self.xsum))

    def getCor(self): # Gets the R squared correlation
        num = (self.count*self.xysum - self.xsum*self.ysum) * (self.count*self.xysum - self.xsum*self.ysum)
        den = (self.count*self.x2sum - self.xsum*self.xsum) * (self.count*self.y2sum - self.ysum*self.ysum)
        return num / den

    def debug(self):
        print "X sum " + str(self.xsum)
        print "Y sum " + str(self.ysum)
        print "XY sum " + str(self.xysum)
        print "X^2 sum " + str(self.x2sum)
        print "Y^2 sum " + str(self.y2sum)
        print "Count " + str(self.count)


def main():

    print ""
    print('Calibrating the sonar to form linear best fit')
    print('Stand certain distance away from sensor and record distance')
    print('Can enter as many or as few distances as needed')
    print('To end calibration enter distance of 0 ')
    print ""

    looping = True

    calculator = SonarCalibration()

    while looping:
        choice = raw_input('Enter distance of object from sensor in inches:')
        if choice[0] == '0':
            looping = False
        elif choice == "-1":
            calculator.readAna()
        else:
            distance = int(choice)
            calculator.addPoint(distance)
            #calculator.debug()

    print('Calibration Complete')
    print('R squared value is ' + str(calculator.getCor()))
    choice2 = raw_input('Do you want to save calibrated data? (y/n)')

    if choice2[0] == 'y':
        writer = open("SonarCalibrationData.txt","w")
        writer.write(str(calculator.getSlope()) + " " + str(calculator.getIntersept()))
        writer.close()
        print "Calibration saved"
    else:
        print "Calibration not saved"


if __name__ == "__main__":
    main()