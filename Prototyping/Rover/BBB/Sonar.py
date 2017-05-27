import math
import serial
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.ADC as ADC
from time import sleep
UART.setup("UART1")
ser = serial.Serial('/dev/ttyO1', 9600)


class Sonar:
    def __init__(self, pin):
        ADC.setup()
        self.maxAnaVal = 0.8
        # Reads the data from SonarCalibrationData.txt
        # The data is in the form "<slope> <intercept>"
        reader = open("SonarCalibrationData.txt", "r")
        values = reader.readline().split()
        reader.close()
        self.slope = float(values[0])
        self.intersecpt = float(values[1])
        self.pin = pin


    def readAna(self): # Get raw analog value from sensor
        readVal = ADC.read(self.pin)
        return readVal

    def readDisInch(self):  # Calculates distance in inches
        readVal = ADC.read(self.pin)
        readVal = (readVal * self.slope) + self.intersecpt # Calculated through linear best fit
        return readVal

    def readDisCm(self): # Calculates distance in centimeters
        readVal = ADC.read(self.pin)
        readVal = ((readVal * self.slope) - self.intersecpt) * 2.54  # Calculated through linear best fit
        return readVal

    def readDisM(self):  # Calculates distance in meters
        readVal = self.readDisCm()/ 100  # Calculated through linear best fit
        return readVal

    def getMaxDisM(self): # Returns max distance readble in meters
        return (self.maxAnaVal * self.slope + self.intersecpt) * 0.0254

    # Returns the horizontal distance in inches to object given angle
    # The angle is a value from 0 - 90 with 0 straight forward and 90 straight down
    def readTrueDisInch(self, angle):
        return math.cos(angle) * self.readDisInch()

    # Returns the horizontal distance in meters to object given angle
    # The angle is a value from 0 - 90 with 0 straight forward and 90 straight down
    def readTrueDisM(self, angle):
        return math.cos(angle) * self.readDisM()