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


# Distance and bearing stuff writen by Brian
# 5/17/2017

# returns the distance in meters between two GPS coords
# uses the haversine formula
# start and end are tuples of floats representing a GPS coord
# reference: http://www.movable-type.co.uk/scripts/latlong.html
def dist(start, end):
    R = 6371000
    phi_1 = math.radians(start[0])
    phi_2 = math.radians(end[0])
    delta_phi = math.radians(end[0] - start[0])
    delta_lambda = math.radians(end[1] - start[1])
    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(
        delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def unscaledDist(start, end):
    distLat = (end[0] - start[0])
    distLong = (end[1] - start[1])
    return (((distLat ** 2) + (distLong ** 2))**.5)*100000

# returns the initial bearing of the great circle between two GPS coords
# start and end are tuples of floats representing a GPS coord
# returns the result in degrees
# reference: http://www.movable-type.co.uk/scripts/latlong.html
def bearing(start, end):
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
def point_at_end(start, brng, dist):
    R = 6371000
    start_rad = (math.radians(start[0]), math.radians(start[1]))
    b_rad = math.radians(brng)
    phi_2 = math.asin(
        math.sin(start_rad[0]) * math.cos(dist / R) + math.cos(start_rad[0]) * math.sin(dist / R) * math.cos(brng))
    lambda_2 = start[1] + math.atan2(math.sin(brng) * math.sin(dist / R) * math.cos(start_rad[0]),
                                     math.cos(dist / R) - math.sin(start_rad[0]) * math.sin(phi_2))
    return math.degrees(phi_2), (lambda_2 + 540) % 360 - 180


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

def scale_coords(coord, reference):
      """
      Scales GPS coordinates into meter coordinates
      Coordinates are given as (lat, long) in degrees
      Args:
         coord (Tuple of (float, float)): The coordinates to convert
         reference (Tuple of (float, float)): The reference point to be converted to (0, 0)
      Returns (Tuple of (float, float)): (x, y) coordinates in meters
      """
      xDistance = distance(coord[0], coord[1], coord[0], reference[1])
      if coord[1] < reference[1]:
          xDistance = -xDistance
      yDistance = distance(coord[0], coord[1], reference[0], coord[1])
      if coord[0] < reference[0]:
          yDistance = -yDistance
      return (xDistance, yDistance)