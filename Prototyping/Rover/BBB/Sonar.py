import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)


class Sonar:
    def __init__(self):
        ADC.setup()
        self.maxAnaVal = 0.8

    def readAna(self): # Get raw analog value from sensor
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

