import mag as MAG
import gps as GPS
import Utils
import Adafruit_BBIO.ADC as ADC
from time import sleep, time
from threading import Thread

# The number of seconds before a GPS reading is considered to be invalid
STALE_GPS_TIME = 2.0

class Navigation:
    """
    Object for managing navigation (magnetometer, GPS, potentiometer)

    Attributes:
        mag (MAG.Magnetometer), gps (GPS.GPS): Objects for managing
            magnetometer and GPS.
        POT_PIN (str): The name of the pin the potentiometer is connected to.
        POT_LEFT, POT_RIGHT, POT_MIDDLE (float): The potentiometer readings
            when the joint is at the leftmost, straight, and rightmost
            respectively.
        POT_TOL (float): Currently unused. Maybe some kind of tolerance value.
            Maybe we should remove this?
    """
    def __init__(self, pot_left, pot_middle, pot_right, pot_tol, pot_pin):
        """
        Args:
            pot_left, pot_middle, pot_right (float): The potentiometer readings
                when the joint is at the leftmost, straight, and rightmost
                respectively.
            pot_tol (float): Currently unused. Maybe some kind of tolerance
                value. Maybe we should remove this?
            pot_pin (str): The name of the pin the potentiometer is connected to.
            lastGPS (tuple of (float, float)): Lastest GPS reading
            lastGPSTime (float): timestamp when lastGPS was read
        """
        self.mag = MAG.Magnetometer()
        self.gps = GPS.GPS()
        self.POT_PIN = pot_pin
        self.POT_LEFT = float(pot_left)
        self.POT_RIGHT = float(pot_right)
        self.POT_MIDDLE = float(pot_middle)
        self.POT_TOL = float(pot_tol)
        self.lastGPS = None
        self.lastGPSTime = time() - STALE_GPS_TIME * 2
        self.prevGPS = [(0,0), (1,1), (2,2), (3,3), (4,4)]
        thread = Thread(target = self.updateGPS)
        thread.daemon = True
        thread.start()

    # returns a float of how far from straight the potentiomer is. > 0 for Right, < 0 for left
    # returns -1 if error
    def readPot(self):
        result = self.POT_MIDDLE - ADC.read(self.POT_PIN)
        if result > self.POT_MIDDLE - self.POT_RIGHT or result < self.POT_MIDDLE - self.POT_LEFT:
            return -1
        return result

    # returns heading of front body or -1 if error
    def getMag(self):
        rawMag = self.mag.read()
        pot = self.readPot()
        angle = Utils.translateValue(pot, self.POT_LEFT - self.POT_MIDDLE, self.POT_RIGHT - self.POT_MIDDLE, -40, 40)
        # returns the raw reading minus the angle from pot
        # minus 170 for the angle the mag is mounted
        return (rawMag + angle - 200) % 360

    def getGPS(self):
        return self.lastGPS

    # Periodically updates the GPS data
    def updateGPS(self):
        while True:
            print self.prevGPS
            gps = self.gps.getCoords()
            if gps is not None:
                gpsFailure = False
                for i in range(1,5):
                    if self.prevGPS[0] == self.prevGPS[i]:
                        gpsFailure = True
                if gpsFailure:
                    print "---------- GPS ERROR --- RESTARTING GPS-----------"
                    self.gps = GPS.GPS()
                    self.prevGPS = [(0,0), (1,1), (2,2), (3,3), (4,4)]
                else:
                    for i in range(0,4):
                        self.prevGPS[i] = self.prevGPS[i + 1]
                    self.prevGPS[4] = gps
                self.lastGPS = gps
            sleep(0.2)

    def get_pot_left(self):
        return self.POT_LEFT

    def get_pot_right(self):
        return self.POT_RIGHT

    def get_pot_middle(self):
        return self.POT_MIDDLE
