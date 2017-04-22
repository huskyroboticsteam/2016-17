import math
import Utils
import mag as MAG
import gps as GPS
import Adafruit_BBIO.ADC as ADC

class Navigation:
    """
    Object for managing navigation (magnetometer, GPS, potentiometer)

    Attributes:
        destinations (list of tuple of (float, float)): List of GPS coordinates
            to travel to.
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
        """
        # list of GPS coords to travel to
        # TODO: actually use this
        self.destinations = []
        self.mag = MAG.Magnetometer()
        self.gps = GPS.GPS()
        self.POT_PIN = pot_pin
        self.POT_LEFT = float(pot_left)
        self.POT_RIGHT = float(pot_right)
        self.POT_MIDDLE = float(pot_middle)
        self.POT_TOL = float(pot_tol)


    # returns a float of how far from straight the potentiomer is. > 0 for Right, < 0 for left
    # returns -1 if error
    def readPot(self):
        result = self.POT_MIDDLE - ADC.read(self.POT_PIN)
        if result > self.POT_MIDDLE - self.POT_RIGHT or result < self.POT_MIDDLE - self.POT_LEFT:
            print result
            return -1
        return result

    # returns heading of front body or -1 if error
    def getMag(self):
        rawMag = self.mag.read()
        print "back: " + str(rawMag)
        pot = self.readPot()
        angle = Utils.translateValue(pot, self.POT_LEFT - self.POT_MIDDLE, self.POT_RIGHT - self.POT_MIDDLE, -40, 40)
        print "front: " + str((rawMag + angle) % 360)
        return (rawMag + angle) % 360

    # returns gps data
    def getGPS(self):
        return self.gps.getCoords()

    # find distance between two points using the haversine formula
    def distance(self, desLong, desLat):
        gps = GPS.GPS()
        cord = gps.getCoords()
        lat1 = math.radians(cord[0])
        long1 = math.radians(cord[1])
        lat2 = math.radians(desLat)
        long2 = math.radians(desLong)
        r = 6371  # radius of earth
        dlat = lat2 - lat1
        dlon = long2 - long1

        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2*math.asin(math.sqrt(a))

        return r * c  # kilometers

    # TODO Return a bool determining if there is something in way
    #      If false, there is no obstacle within checkingDistance of rover sensor
    def isObstacle(self):
        return False

    def get_pot_left(self):
        return self.POT_LEFT

    def get_pot_right(self):
        return self.POT_RIGHT

    def get_pot_middle(self):
        return self.POT_MIDDLE

    # appends a destination to the list of destinations
    def append_destiniation(self, dest):
        self.destinations.append(dest)
