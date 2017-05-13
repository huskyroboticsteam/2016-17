import math
import os
import urllib
from PyQt4 import QtCore
import Utility


class Generator(QtCore.QThread):
    """
    Downloads static map files through either the Bing or Google Map APIs. Allows for the user to specify
    the folder where all of the map tiles are stored.
    """

    success = False
    name = None
    lat = None
    lng = None

    def __init__(self, tile_size, api, num_tiles):
        super(self.__class__, self).__init__()
        self.TILE_SIZE = tile_size
        self.api = api
        self.num_tiles = num_tiles

    def retrieve_online_image(self, local_path, location, i, fname):

        """
        Retrieves a single map tile from the Bing or Google Static Maps API and stores it on the local machine
        :param local_path: Folder name for a specific map zoom level
        :param location: Specifies where the center tile is dependent on API
        :param i: While tile of a specific map zoom level we are on
        :param fname: Root folder name for entire map
        :return: None
        """

        if self.api == "Bing":
            baseUrl = "http://dev.virtualearth.net/REST/V1/"
            callType = "Imagery/map/AerialWithLabels/"
            apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"
        else:
            baseUrl = "https://maps.googleapis.com/maps/api/staticmap"
            callType = "?maptype=hybrid&scale=1&format=jpg"
            apiKey = "&key=AIzaSyClTno1x7g7MPiUP-kIJhmUst5EQLldS48"

        queryString = baseUrl + callType + location + apiKey
        print queryString

        # Checks if the folder exists, if it doesn't create the folder
        if not os.path.exists(fname):
            os.mkdir(fname)

        # Append the folder name to the local path
        local_path = fname + "/" + local_path

        # Checks if the folder exists, if it doesn't create the folder
        if not os.path.exists(local_path):
            os.mkdir(local_path)

        # Query the server and save the image to the given path
        urllib.urlretrieve(queryString, os.path.join(local_path, "map" + str(i) + ".jpg"))

    def generate_single_map(self, zoom, lat, lng, tiles, fname):

        """
        Generates a single zoom level of a map centered on a specified lat and lng
        :param zoom: The zoom level of the map (see API docs for details)
        :param lat: The latitude coordinate in decimal form
        :param lng: The longitude coordinate in decimal form
        :param tiles: The number of tiles on this map (must be a square of an odd number, e.g.: 25, 49)
        :param fname: The root folder name for the map
        :return: None
        """

        zoom = int(zoom)
        lat = float(lat)
        lng = float(lng)
        tiles = int(tiles)

        x, y = Utility.calculate_corner_center(zoom, lat, lng, tiles, self.TILE_SIZE)
        # Remember the left-hand edge of the map
        original_x = x

        # 1 indexed loop so the math makes more sense
        for i in range(1, tiles + 1, 1):
            lat, lng = Utility.convert_pixels_to_degrees(zoom, x, y)

            if self.api == "Bing":
                location = str(lat) + "," + str(lng) + "/" + str(zoom) + "?mapSize=" + str(self.TILE_SIZE) + "," + \
                          str(self.TILE_SIZE)
            else:
                location = "&center=" + str(lat) + "," + str(lng) + "&zoom=" + str(zoom) + "&size=" + str(self.TILE_SIZE) + "x" + \
                str(self.TILE_SIZE)

            self.retrieve_online_image(str(zoom), location, i, fname)

            # At the edge of the square of tiles
            if i % math.sqrt(tiles) == 0:
                y += self.TILE_SIZE
                x = original_x
            else:
                x += self.TILE_SIZE

    def run(self):

        """
        Generates a map with zoom levels 15 - 19 centered on a given latitude and longitude
        :param name: Name of root folder for map
        :param lat: The latitude coordinate in decimal form
        :param lng: The longitude coordinate in decimal form
        :return: Boolean indicating whether the map successfully generated
        """

        name = str(self.name)
        lat = str(self.lat)
        lng = str(self.lng)

        # Don't try to download maps if the input is invalid
        if Utility.is_valid_coord(lat) and Utility.is_valid_coord(lng) and Utility.is_valid_file_name(name):

            # Creates / overwrites a text file and stores the center (lat, lng) and folder name of map generated
            f = open(name + ".dat", "w")
            f.write(name + "\n")
            f.write(str(self.TILE_SIZE) + "\n")
            f.write(str(self.TILE_SIZE) + "\n")
            for i in range(0, len(self.num_tiles)):
                f.write(str(self.num_tiles[i]) + "\n")
            f.write(lat + "\n")
            f.write(lng + "\n")
            f.close()

            # Generate all zoom levels of the map 15 - 19
            for i in range(15, 20):
                self.generate_single_map(i, lat, lng, self.num_tiles[i - 15], name)

            self.success = True

        else:
            print "Some input is invalid"
            self.success = False

