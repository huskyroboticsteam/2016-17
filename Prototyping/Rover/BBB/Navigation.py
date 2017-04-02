import math
import Utils
import mag as MAG
import gps as GPS
import Adafruit_BBIO.ADC as ADC

class Navigation:
    """
    Object for managing navigation (e.g. potentiometer, magnetometer, obstacle
    avoidance, GPS, autopilot)

    Attributes:
        auto (bool): True if currently in autopilot mode.
        destinations (list of tuple of (float, float)): List of GPS coordinates
            to travel to.
        scannedHeadings (list of tuple of (float, bool)): List of tuples with
            headings and bools determining if there's an obstacle there.
        mag (MAG.Magnetometer), gps (GPS.GPS): Objects for managing
            magnetometer and GPS.
        POT_PIN (str): The name of the pin the potentiometer is connected to.
        POT_LEFT, POT_RIGHT, POT_MIDDLE (float): The potentiometer readings
            when the joint is at the leftmost, straight, and rightmost
            respectively.
        POT_TOL (float): Currently unused. Maybe some kind of tolerance value.
            Maybe we should remove this?
        avoidingObs (bool), checkingDistance (int): Someone who knows what
            these are for please document them.
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
        # autopilot
        self.auto = True
        # list of GPS coords to travel to
        self.destinations = []
        # list of tuple with heading and bool determining if obstacle
        self.scannedHeadings = []
        self.mag = MAG.Magnetometer()
        self.gps = GPS.GPS()
        self.POT_PIN = pot_pin
        self.POT_LEFT = float(pot_left)
        self.POT_RIGHT = float(pot_right)
        self.POT_MIDDLE = float(pot_middle)
        self.POT_TOL = float(pot_tol)
        self.avoidingObs = False
        self.checkingDistance = 2


    # returns a float of how far from straight the potentiomer is. > 0 for Right, < 0 for left
    # returns -1 if error
    def readPot(self):
        result = self.POT_MIDDLE - ADC.read(self.POT_PIN)
        if result > self.POT_MIDDLE - self.POT_RIGHT or result < self.POT_MIDDLE - self.POT_LEFT:
            print result
            return -1
        return result

    # returns heading of front body or -1 if error
    # TODO: Use code from Orientation.py and test it.
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

    # calculates the desired heading
    # returns a value between 0 and 360 inclusive
    def calculateDesiredHeading(self):
        currLocation = self.gps.getCoords()
        destination = self.destinations[0]
        x_distance = self.distance(destination[0], currLocation[1])
        y_distance = self.distance(currLocation[0], destination[1])
        if (y_distance != 0):
            theta = math.atan2(x_distance, y_distance)
            return Utils.translateValue(self, theta, -1 * math.pi, math.pi, 0, 360)
        else:
            return 0

    # find distance between two points using the haversine formula
    def distance(self, desLong, desLat):
        gps = GPS.GPS()
        cord = gps.getCoords()
        lat1 = self.radGPS(cord[0])
        long1 = self.radGPS(cord[1])
        lat2 = self.radGPS(desLat)
        long2 = self.radGPS(desLong)
        r = 6371  # radius of earth
        dlat = lat2 - lat1
        dlon = long2 - long1

        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2*math.asin(math.sqrt(a))

        return r * c  # kilometers

    # takes the dec min format and converts it to radians
    def radGPS(self, val):
        return math.radians(val)

    # calculates desired new GPS coordinate based on distance
    # from current GPS location and current heading in degrees
    def calculateDesiredNewCoordinate(self, currHeading, distance):
        theta = Utils.translateValue(self, currHeading, 0, 360, 0, 2 * math.pi)
        x = distance * math.cos(theta)
        y = distance * math.sin(theta)
        coords = (x, y)
        return coords

    # returns a turn value from -100 to 100 based on the difference between the current heading and the desired heading
    def calculateDesiredTurn(self, curHeading, desiredHeading):
        difHeading = abs(curHeading - desiredHeading)
        if ((curHeading > desiredHeading and difHeading > 180) or
            (curHeading < desiredHeading and difHeading < 180)):
            #turn right
            return Utils.translateValue(difHeading % 180, 0, 180, 0, 10)
        else:
            #turn left
            return -1 * Utils.translateValue(difHeading % 180, 0, 180, 0, 10)

    # TODO Return a bool determining if there is something in way
    #      If false, there is no obstacle within checkingDistance of rover sensor
    def isObstacle(self):
        return False

    # Adds a (heading, isObsticalVal) pair to scannedHeadings
    def appendScannedHeadings(self):
        self.scannedHeadings.append(self.getMag(), self.isObstacle())

    # Checks to see if first value in scannedHeadings is a "temp" value
    # If so then just replace it
    def checkIfAvoidingObs(self, heading):
        if self.avoidingObs:
            self.destinations.pop(self, 0)
            self.destinations.insert(0, self.calculateDesiredNewCoordinate(heading, self.checkingDistance))
        else:
            self.destinations.insert(0, self.calculateDesiredNewCoordinate(heading, self.checkingDistance))

    # Will calculate a heading closest to center and add destination to destination list
    def addDestination(self):
        # Not used now but might need it if not path forward
        centerHeading = self.scannedHeadings.pop(self, int(len(self.scannedHeadings) / 2))[0]
        # Determine path closest to center with no obstacle
        # Removes values from center of array outward
        inLoop = True
        possibleHeadings = []
        while (inLoop):
            middleHeading = int(len(possibleHeadings) / 2)
            tempHeading = self.scannedHeadings.pop(self, middleHeading)
            if self.scannedHeadings[0] is None:
                inLoop = False
            # Check for next value to the right of center
            if (not tempHeading[1]):
                self.scannedHeadings = []
                self.checkIfAvoidingObs(tempHeading[0])
            # Get new heading to check
            tempHeading = possibleHeadings.pop(self, middleHeading -1)
            if (self.scannedHeadings[0] is None):
                inLoop = False
            # Check for next value to the left of center
            if (not tempHeading[1]):
                self.scannedHeadings = []
                self.checkIfAvoidingObs(tempHeading[0])
        # TODO: What to do if there is no path forward?

    # returns True for autopilot False for manual control
    def getAuto(self):
        return self.auto

    # sets the Autopilot
    def setAuto(self, autoVal):
        self.auto = autoVal

    def get_pot_left(self):
        return self.POT_LEFT

    def get_pot_right(self):
        return self.POT_RIGHT

    def get_pot_middle(self):
        return self.POT_MIDDLE

    # appends a destination to the list of destinations
    def append_destiniation(self, dest):
        self.destinations.append(dest)
