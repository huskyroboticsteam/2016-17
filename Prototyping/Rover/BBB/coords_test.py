import math

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
    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# returns the initial bearing of the great circle between two GPS coords
# start and end are tuples of floats representing a GPS coord
# returns the result in degrees
# reference: http://www.movable-type.co.uk/scripts/latlong.html
def bearing(start, end):
    start_rad = (math.radians(start[0]), math.radians(start[1]))
    end_rad = (math.radians(end[0]), math.radians(end[1]))
    y = math.sin(end_rad[1] - start_rad[1]) * math.cos(end_rad[0])
    x = math.cos(start_rad[0]) * math.sin(end_rad[0]) - math.sin(start_rad[0]) * math.cos(end_rad[0]) * math.cos(end_rad[1] - start_rad[1])
    return (math.degrees(math.atan2(y, x)) + 360) % 360


# returns the GPS coord of the point dist away from start along bearing
# start is tuple of floats representing a GPS coord
# bearing is a float representing a compass direction in degrees
# dist is a distance in meters
def point_at_end(start, brng, dist):
    R = 6371000
    start_rad = (math.radians(start[0]), math.radians(start[1]))
    b_rad = math.radians(brng)
    phi_2 = math.asin(math.sin(start_rad[0]) * math.cos(dist / R) + math.cos(start_rad[0]) * math.sin(dist / R) * math.cos(brng))
    lambda_2 = start[1] + math.atan2(math.sin(brng) * math.sin(dist / R) * math.cos(start_rad[0]),
                                     math.cos(dist / R) - math.sin(start_rad[0]) * math.sin(phi_2))
    return math.degrees(phi_2), (lambda_2 + 540) % 360 - 180

coord1 = (47.651269, -122.306035)
coord2 = (47.652599, -122.307062)
coord3 = (47.659936, -122.306323)

dist_1_2 = dist(coord1, coord2)
dist_2_1 = dist(coord2, coord1)
dist_3_1 = dist(coord3, coord1)
dist_1_3 = dist(coord1, coord3)
dist_2_3 = dist(coord2, coord3)
dist_3_2 = dist(coord3, coord2)

bear_1_2 = bearing(coord1, coord2)
bear_1_3 = bearing(coord1, coord3)

print(dist_1_2)
print(dist_2_1)

print(bear_1_2)
print(bear_1_3)

print point_at_end(coord1, bear_1_2, dist_1_2)
print coord2

