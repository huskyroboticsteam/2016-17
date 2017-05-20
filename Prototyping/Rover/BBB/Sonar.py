import math
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
        reader = open("SonarCalibrationData.txt", "r")
        values = reader.readline().split()
        reader.close()
        self.slope = float(values[0])
        self.intersecpt = float(values[1])


    def readAna(self): # Get raw analog value from sensor
        readVal = ADC.read("AIN6")
        return readVal

    def readDisInch(self):  # Calculates distance in inches
        readVal = ADC.read("AIN6")
        readVal = (readVal * self.slope) + self.intersecpt # Calculated through linear best fit
        return readVal

    def readDisCm(self): # Calculates distance in centimeters
        readVal = ADC.read("AIN6")
        readVal = ((readVal * self.slope) - self.intersecpt) * 2.54  # Calculated through linear best fit
        return readVal

    def readDisM(self):  # Calculates distance in meters
        readVal = self.readDisCm()/ 100  # Calculated through linear best fit
        return readVal

    def getMaxDisM(self): # Returns max distance readble in meters
        return self.maxAnaVal * self.slope + self.intersecpt

    def readTrueDisInch(self, angle):
        return math.cos(angle) * self.readDisInch()