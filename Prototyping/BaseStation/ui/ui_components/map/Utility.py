import math

import Utility


def calculate_corner_center(zoom, lat, lng, tiles, tile_size):
    # Find how many tiles up and left the top left tile is at from the center
    tiles_to_corner = (math.sqrt(tiles) - 1) / 2

    # Move over to the top left center position on the zoom_location grid
    x, y = Utility.convert_degrees_to_pixels(zoom, lat, lng)
    x -= tiles_to_corner * tile_size[0]
    y -= tiles_to_corner * tile_size[1]

    return x, y


# Accepts pixel x and y from the zoom_level dependent Bing coordinate system
# Returns a latitude and longitude
def convert_pixels_to_degrees(zoom, pixelX, pixelY):
    # Converts to coordinate system determined by map density
    # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

    x = (pixelX / (256 * math.pow(2, zoom))) - 0.5
    y = 0.5 - (pixelY / (256 * math.pow(2, zoom)))

    lat = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
    lng = 360 * x

    return lat, lng


# Accepts a latitude and longitude
# Returns pixel coordinates in the zoom_level dependent Bing coordinate system
def convert_degrees_to_pixels(zoom, lat, lng):
    # Converts to coordinate system determined by map density
    # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

    lat = float(lat)
    lng = float(lng)

    sinLatitude = math.sin(lat * math.pi / 180)

    x = (lng + 180) / 360
    y = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi))

    pixelX = int((x * 256 * math.pow(2, zoom)) + 0.5)
    pixelY = int((y * 256 * math.pow(2, zoom)) + 0.5)

    return pixelX, pixelY


def is_valid_coord(coord):

    # If the user inputs garbage values like 'abcde' for lat or lng then return false
    try:
        flo = float(coord)
    except ValueError:
        return False
    else:
        return -180 <= flo <= 180


def is_valid_file_name(name):
    return name != ""
