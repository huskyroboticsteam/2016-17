import re

# Classes and methods related to GPS coordinates and converting.

# Class for the degree, minute, second coordinate structure.
class degreeMin:
    def __init__(self, degree, minute = 0.0, seconds = 0.0): # If minutes or seconds unprovided, go without
        if(degree == ""):
            self.degrees = "0"
        else:
           self.degrees = degree
        if(minute == ""):
            self.min = "0"
        else:
            self.min = minute
        if(seconds == ""):
            self.sec = "0"
        else:
            self.sec = seconds

    def toDecimal(self):
        if self.degrees > 0.0: # If degrees value is positive, add minutes and seconds.
            result = float(self.degrees) + (float(self.min) / 60.0) + (float(self.sec) / 3600.0)
        if self.degrees <= 0.0: # If degrees value is negative, need to subtract minutes and seconds.
            result = float(self.degrees) - (float(self.min) / 60.0) - (float(self.sec) / 3600.0)
        return result

#defines a new class to store coordinates
#this class stores the string representations of GPS coordinates that can be converted to pixels when needed.
#TODO: fix coordinate return methods
#TODO: create mapping function
class CoordinatePair: # Contains lat and long objects
    def __init__(self):
        self.lat = degreeMin(0, 0, 0)
        self.long = degreeMin(0, 0, 0)
    #converts lat to a x position for display
    def xPos(self):
        return int(self.lat.toDecimal())
    #converts long to a y position for display
    def yPos(self):
        return int(self.long.toDecimal())
    def toString(self):
        return str(self.lat.degrees) + "." + str(self.lat.min) + "." + str(self.lat.sec) + "," + str(self.long.degrees) + "." + str(self.long.min) + "." + str(self.long.sec)

# Austin's coordinate conversion class
class Coordinates:
    def __init__(self, current_string):
        s = current_string.split(',')
        print "split: " + str(s)
        if len(s) < 2:
            self.status = False
        else:
            tempLat = self.splitInput(s[0])
            tempLong = self.splitInput(s[1])
            print "templat: " + str(tempLat)
            print "templong: " + str(tempLong)
            self.latitude = self.format(tempLat)
            self.longitude = self.format(tempLong)
            print self.latitude
            print self.longitude
            if self.latitude >= 90 or self.latitude <= 0 or self.longitude >= 0 or self.longitude <= -180: # Make sure input lat, long are sensible for northern, western hemisphere (UW and Utah)
                self.status = False
            else:
                self.status = True

    # separates out all non-numeric values
    def splitInput(self, s):
        temp = filter(None, re.split(r'[^-\d.]+', s))
        return self.castToFloat(temp)

    def castToFloat(self, arr):
        return [float(i) for i in arr]

    def format(self, arr):
        if len(arr) == 1: # If the input was just decimal, no minute or second entry
            return float(arr[0]) # returns float if it is in standard format
        elif len(arr) == 2: # If degrees and minutes provided...
            degreeMinCoords = degreeMin(arr[0],arr[1])
            return degreeMinCoords.toDecimal() # Use Brian's method to convert DMS format to decimals
        elif len(arr) >= 3:
            degreeMinSecCoords = degreeMin(arr[0],arr[1],arr[2])
            return degreeMinSecCoords.toDecimal()

# --------------------------------------------------------------------------------------

# Brian's coordinate conversion function
def convertCoords(current_string):

    """
    :rtype : CoordinatePair
    """

    commaSeen = False
    coordRead = ""
    newCoord = CoordinatePair()
    #loops through all characters in the text box
    for chars in range(len(current_string) + 1):
        #print range(len(current_string) + 1)
        #print len(current_string)
        if chars == len(current_string): # If final character in current_string has been reached...
            counter = 0
            long = ""
            for i in range(len(coordRead)): # Build the longitude coordinate.
                long = long + str(coordRead[i])
                if coordRead[i] == ".":
                    counter += 1
                    long = ""
                elif counter == 0:
                    newCoord.long.degrees = long
                elif counter == 1:
                    newCoord.long.min = long
                elif counter == 2:
                    newCoord.long.sec = long
        elif current_string[chars] == ",": # If a comma has been reached...
            if not commaSeen: # If this is the first comma...
                counter = 0
                lat = ""
                for i in range(len(coordRead)): # Build the latitude coordinate.
                    lat = lat + str(coordRead[i])
                    if coordRead[i] == ".":
                        counter += 1
                        lat = ""
                    elif counter == 0:
                        newCoord.lat.degrees = lat
                        # Update after every single character?
                    elif counter == 1:
                        newCoord.lat.min = lat
                    elif counter == 2:
                        newCoord.lat.sec = lat
                coordRead = ""
                commaSeen = True # Ignore any further commas.
        else: # If it's a number or period (not a separator)...
            coordRead = coordRead + str(current_string[chars]) # Add current character to the string
    return newCoord