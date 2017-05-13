import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
import Sonar
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)

'''
Prints the distance from sensor in cm

'''

class SonarTest:
    def __init__(self):
        ADC.setup()

    '''
    def read(self): # Still trying to get serial to work
                    # It dosn't work
        try:
            # flush twice to make sure nothing is clogged
            ser.flushInput()
            ser.flushInput()
            readVal = ser.readline()
            print(readVal)

        except:
            print ("Cant read")
            pass

    def readAna(self): # Get raw analog value from sensor
        self.localSonar.
        readVal = ADC.read("AIN6")
        print(readVal)


    def readDisInch(self):  # Calculates distance in inches
        readVal = ADC.read("AIN6")
        readVal = (readVal * 370.3) - 57.83 # Calculated through linear best fit
        print(readVal)

    def readDisCm(self): # Calculates distance in centimeters
        readVal = ADC.read("AIN6")
        readVal = ((readVal * 370.3) - 57.83) * 2.54  # Calculated through linear best fit
        print(readVal)
    '''



def main():
    choice = raw_input('Choose Read Value: \n 0: Analog \n 1: Inches \n 2: Centimeters \n')
    caller = Sonar.Sonar()
    if choice[0] == '0':
        while True:
            print str(caller.readAna())
    elif choice[0] == '1':
        while True:
            print str(caller.readDisInch())
    elif choice[0] == '2':
        while True:
            print str(caller.readDisCm())
    else:
        while True:
            print str(caller.readDisAna())

if __name__ == "__main__":
    main()