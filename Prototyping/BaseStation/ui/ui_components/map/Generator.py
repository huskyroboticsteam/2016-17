import math
import os
import urllib

import Utility


class Generator:
    def __init__(self, tile_size, image_tiles):
        self.TILE_SIZE = tile_size
        self.image_tiles = image_tiles

    def retrieve_online_image(self, local_path, location, i, fname):
        baseUrl = "http://dev.virtualearth.net/REST/V1/"
        callType = "Imagery/map/AerialWithLabels/"
        apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"

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

            location = str(lat) + "," + str(lng) + "/" + str(zoom) + "?mapSize=" + str(self.TILE_SIZE[0]) + "," + \
                       str(self.TILE_SIZE[1])

            self.retrieve_online_image(str(zoom), location, i, fname)

            # At the edge of the square of tiles
            if i % math.sqrt(tiles) == 0:
                y += self.TILE_SIZE[1]
                x = original_x
            else:
                x += self.TILE_SIZE[0]

    def generate_maps(self):

        lat = ""
        lng = ""
        name = ""

        while True:
            # Take input
            lat = raw_input("Select Center Latitude: ")
            lng = raw_input("Select Center Longitude: ")
            name = raw_input("map name: ")

            if Utility.is_valid_coord(lat) and Utility.is_valid_coord(lng) and Utility.is_valid_file_name(name):
                break
            else:
                print "Some input is invalid"

        # Creates / overwrites a text file and stores the center (lat, lng) and folder name of map generated
        f = open(name + ".dat", "w")
        f.write(name + "\n")
        f.write(str(self.TILE_SIZE[0]) + "\n")
        f.write(str(self.TILE_SIZE[1]) + "\n")
        f.write(lat + "\n")
        f.write(lng + "\n")
        f.close()

        # Generate all zoom levels of the map 15 - 19
        for i in range(15, 20):
            self.generate_single_map(i, lat, lng, self.image_tiles[i]["tiles"], name)

        return name

