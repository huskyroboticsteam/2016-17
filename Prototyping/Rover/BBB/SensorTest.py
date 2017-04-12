import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)

'''
Prints the distance from sensor in cm

'''

class SensorTest:
    def __init__(self):
        ADC.setup()

    def read(self): # Still trying to get serial to work
        try:
            # flush twice to make sure nothing is clogged
            ser.flushInput()
            ser.flushInput()
            readVal = ser.readline()
            print(readVal)

        except:
            print ("Cant read")
            pass

    def readAna(self):
        readVal = ADC.read("AIN6")
        print(readVal)


    def readDis(self): # Calculates distance in inches
        readVal = ADC.read("AIN6") # Trust the numbers
        readVal -= 0.197
        readVal = (readVal / 0.0064) * 2.0 * (10.0/9.0)
        readVal += 8.0
        readVal = readVal * (1/0.8915)
        print(readVal)


    def readDis2(self):  # Calculates distance in inches
        readVal = ADC.read("AIN6")  # Trust the numbers
        readVal = (readVal * 370.3) - 57.83
        print(readVal)


caller = SensorTest()
while(1):
    caller.readDis2()
