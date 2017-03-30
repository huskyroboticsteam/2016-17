import math
import Utility


def calculate_corner_center(zoom, lat, lng, tiles, tile_size):
    """
    Calculates how many tiles the top left tile's center is away from the map's center
    :param zoom: The zoom level of the map
    :param lat: The latitude of the map's center
    :param lng: The longitude of the map's center
    :param tiles: The number of tiles total in the map with the specified zoom level
    :param tile_size: The size of either the width or height of the tile (since they are square)
    :return: Returns a x and y coordinate in the Mercator projection coordinate system
    """
    # Find how many tiles up and left the top left tile is at from the center
    tiles_to_corner = (math.sqrt(tiles) - 1) / 2

    # Move over to the top left center position on the zoom_location grid
    x, y = Utility.convert_degrees_to_pixels(zoom, lat, lng)
    x -= tiles_to_corner * tile_size
    y -= tiles_to_corner * tile_size

    return x, y


def convert_pixels_to_degrees(zoom, pixelX, pixelY):
    """
    Converts to Mercator coordinate system determined by map density
    See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details 
    :param zoom: The zoom level of the map
    :param pixelX: A number in the Mercator coordinate system to convert to longitude
    :param pixelY: A number in the Mercator coordinate system to convert to latitude
    :return: Latitude and longitude separately as numbers
    """

    x = (pixelX / (256 * math.pow(2, zoom))) - 0.5
    y = 0.5 - (pixelY / (256 * math.pow(2, zoom)))

    lat = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
    lng = 360 * x

    return lat, lng


def convert_degrees_to_pixels(zoom, lat, lng):

    """
    Converts to coordinate system determined by map density
    See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details
    :param zoom: The zoom level of the map
    :param lat: A decimal number specifying latitude
    :param lng: A decimal number specifying longitude
    :return: Returns a x and y coordinate in the Mercator projection coordinate system
    """


    lat = float(lat)
    lng = float(lng)

    sinLatitude = math.sin(lat * math.pi / 180)

    x = (lng + 180) / 360
    y = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi))

    pixelX = int((x * 256 * math.pow(2, zoom)) + 0.5)
    pixelY = int((y * 256 * math.pow(2, zoom)) + 0.5)

    return pixelX, pixelY


def is_valid_coord(coord):

    """
    Verifies whether a value is a valid latitude or longitude value
    :param coord: A number representing either latitude or longitude
    :return: Boolean that is true if number is valid
    """

    # If the user inputs garbage values like 'abcde' for lat or lng then return false
    try:
        flo = float(coord)
    except ValueError:
        return False
    else:
        return -180 <= flo <= 180


def is_valid_file_name(name):
    """
    Verifies whether a value is a none empty file name
    :param name: String - name of the file
    :return: True if name is not empty
    """

    return name != ""
