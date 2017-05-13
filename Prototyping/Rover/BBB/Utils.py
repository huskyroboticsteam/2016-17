import math

# translate values from one range to another
def translateValue(value, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    return outMin + (valueScaled * outSpan)


def normalize_angle(angle):
    """
    Args:
        angle (float): the angle in degrees
    Returns (float): the normalized angle such that it is between 0.0 and 360.0

    Isn't this function made simpler by: "return angle % 360.0" ?
    - Jaden Bottemiller

    """
    while angle >= 360.0:
        angle -= 360.0
    while angle < 0.0:
        angle += 360.0
    return angle


# find distance between two points using the haversine formula
def distance(coord1, coord2):
    """
    Finds the distance between two points on earth using the haversine formula
    Args:
        coord1, coord2 (Tuple of (float, float)): The coordinates in the format (lat, long) in degrees.
    Returns (float): The distance between the two points in meters.
    """
    lat1 = math.radians(coord1[0])
    long1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    long2 = math.radians(coord2[1])
    r = 6371000  # radius of earth in meters
    dlat = lat2 - lat1
    dlon = long2 - long1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.asin(math.sqrt(a))

    return r * c  # meters

def scale_coords(self, coord, reference):
      """
      Scales GPS coordinates into meter coordinates
      Coordinates are given as (lat, long) in degrees
      Args:
         coord (Tuple of (float, float)): The coordinates to convert
         reference (Tuple of (float, float)): The reference point to be converted to (0, 0)
      Returns (Tuple of (float, float)): (x, y) coordinates in meters
      """
      xDistance = self.distance(coord[0], coord[1], coord[0], reference[1])
      if coord[1] < reference[1]:
          xDistance = -xDistance
      yDistance = self.distance(coord[0], coord[1], reference[0], coord[1])
      if coord[0] < reference[0]:
          yDistance = -yDistance
      return (xDistance, yDistance)