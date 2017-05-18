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
            return -1
        return result

    # returns heading of front body or -1 if error
    def getMag(self):
        rawMag = self.mag.read()
        pot = self.readPot()
        angle = Utils.translateValue(pot, self.POT_LEFT - self.POT_MIDDLE, self.POT_RIGHT - self.POT_MIDDLE, -40, 40)
        return (rawMag - angle - 140) % 360

    # returns gps data
    def getGPS(self):
        return self.gps.getCoords()

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

    # Distance and bearing stuff writen by Brian
    # 5/17/2017

    # returns the distance in meters between two GPS coords
    # uses the haversine formula
    # start and end are tuples of floats representing a GPS coord
    # reference: http://www.movable-type.co.uk/scripts/latlong.html
    def dist(self, start, end):
        R = 6371000
        phi_1 = math.radians(start[0])
        phi_2 = math.radians(end[0])
        delta_phi = math.radians(end[0] - start[0])
        delta_lambda = math.radians(end[1] - start[1])
        a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(
            delta_lambda / 2) * math.sin(delta_lambda / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # returns the initial bearing of the great circle between two GPS coords
    # start and end are tuples of floats representing a GPS coord
    # returns the result in degrees
    # reference: http://www.movable-type.co.uk/scripts/latlong.html
    def bearing(self, start, end):
        start_rad = (math.radians(start[0]), math.radians(start[1]))
        end_rad = (math.radians(end[0]), math.radians(end[1]))
        y = math.sin(end_rad[1] - start_rad[1]) * math.cos(end_rad[0])
        x = math.cos(start_rad[0]) * math.sin(end_rad[0]) - math.sin(start_rad[0]) * math.cos(end_rad[0]) * math.cos(
            end_rad[1] - start_rad[1])
        return (math.degrees(math.atan2(y, x)) + 360) % 360

    # returns the GPS coord of the point dist away from start along bearing
    # start is tuple of floats representing a GPS coord
    # bearing is a float representing a compass direction in degrees
    # dist is a distance in meters
    def point_at_end(self, start, brng, dist):
        R = 6371000
        start_rad = (math.radians(start[0]), math.radians(start[1]))
        b_rad = math.radians(brng)
        phi_2 = math.asin(
            math.sin(start_rad[0]) * math.cos(dist / R) + math.cos(start_rad[0]) * math.sin(dist / R) * math.cos(brng))
        lambda_2 = start[1] + math.atan2(math.sin(brng) * math.sin(dist / R) * math.cos(start_rad[0]),
                                         math.cos(dist / R) - math.sin(start_rad[0]) * math.sin(phi_2))
        return math.degrees(phi_2), (lambda_2 + 540) % 360 - 180










