import urllib
import os
import math
import MapTile


class Map:
    def __init__(self):
        # Size of all tiles for calculations
        self.TILE_SIZE = [2000, 1500]

        # Current map zoom and center
        self.zoom_level = 15
        self.center = (None, None)

        # Directory where map tiles are located
        self.folderName = None

        # Stores loaded in images
        self.image_tiles = {
            15: {
                "tiles": 9,
                "tilesImages": []
            },
            16: {
                "tiles": 9,
                "tilesImages": []
            },
            17: {
                "tiles": 9,
                "tilesImages": []
            },
            18: {
                "tiles": 25,
                "tilesImages": []
            },
            19: {
                "tiles": 25,
                "tilesImages": []
            }
        }

        # Decides what to run on first opening the program
        new = raw_input("Generate New Map (Y/N): ")

        if new == "Y" or new == "y":
            self.generate_maps()
        else:
            name = raw_input("Map Name? ")
            self.parse_data_file(name)

        self.build_tiles()

    def retrieve_online_image(self, local_path, location, i, fname):
        baseUrl = "http://dev.virtualearth.net/REST/V1/"
        callType = "Imagery/Map/AerialWithLabels/"
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

    def calculate_corner_center(self, zoom, lat, lng, tiles):
        # Find how many tiles up and left the top left tile is at from the center
        tiles_to_corner = (math.sqrt(tiles) - 1) / 2

        # Move over to the top left center position on the zoom_location grid
        x, y = self.convert_degrees_to_pixels(zoom, lat, lng)
        x -= tiles_to_corner * 2000
        y -= tiles_to_corner * 1500

        return x, y

    def generate_single_map(self, zoom, lat, lng, tiles, fname):

        zoom = int(zoom)
        lat = float(lat)
        lng = float(lng)
        tiles = int(tiles)

        x, y = self.calculate_corner_center(zoom, lat, lng, tiles)
        # Remember the left-hand edge of the map
        originalX = x

        # 1 indexed loop so the math makes more sense
        for i in range(1, tiles + 1, 1):
            lat, lng = self.convert_pixels_to_degrees(zoom, x, y)

            location = str(lat) + "," + str(lng) + "/" + str(zoom) + "?mapSize=" + str(self.TILE_SIZE[0]) + "," + \
                       str(self.TILE_SIZE[1])

            self.retrieve_online_image(str(zoom), location, i, fname)

            # At the edge of the square of tiles
            if i % math.sqrt(self.image_tiles[zoom]["tiles"]) == 0:
                y += 1500
                x = originalX
            else:
                x += 2000

    def generate_maps(self):
        # Take input
        lat = raw_input("Select Center Latitude: ")
        lng = raw_input("Select Center Longitude: ")
        name = raw_input("Map name: ")

        # Creates / opens a text file and stores the center (lat, long) and folder name of map generated
        f = open(name + ".dat", "a")
        f.write(name + "\n")
        f.write(lat + "\n")
        f.write(lng + "\n")
        f.close()

        # Set required variables for map open
        self.center = (lat, lng)
        self.folderName = name

        # Generate all zoom levels of the map 15 - 19
        for i in range(15, 20):
            self.generate_single_map(i, lat, lng, self.image_tiles[i]["tiles"], name)

    def zoom_in(self):
        if self.zoom_level < 19:
            self.zoom_level += 1

    def zoom_out(self):
        if self.zoom_level > 15:
            self.zoom_level -= 1

    def parse_data_file(self, name):

        # Open the file for reading
        f = open(name + ".dat", "r")
        dir = f.next().strip('\n')
        lat = f.next().strip('\n')
        lng = f.next().strip('\n')

        print dir
        print lat
        print lng

        # Set the required variables from what was read from the file
        self.center = (lat, lng)
        self.folderName = dir

    def build_tiles(self):
        out = "Loading"

        # Loop through all the zoom levels 15 - 19
        for i in range(15, 20, 1):



            # Decide where the top left tile of the map is
            tiles_to_corner = (math.sqrt(self.image_tiles[i]["tiles"]) - 1) / 2
            pixel = [-2000 * tiles_to_corner, -1500 * tiles_to_corner]

            for j in range(1, self.image_tiles[i]["tiles"] + 1, 1):

                # Appending the folder name before the zoom level to construct the correct file path
                path = self.folderName + "/" + str(i)

                # Make a tile and add it to the list of tiles
                tile = MapTile.MapTile(path, "map" + str(j) + ".jpg", pixel[0], pixel[1])
                self.image_tiles[i]["tilesImages"].append(tile)

                # Decide whether or not the tile is initially on screen
                self.set_visibility(tile)

                # Move back to the left hand side once we reach the edge of the square
                if j % math.sqrt(self.image_tiles[i]["tiles"]) == 0:
                    pixel[0] = -2000 * tiles_to_corner
                    pixel[1] += 1500
                else:
                    pixel[0] += 2000

            out += "."
            print out

    # Chooses whether to set have the tile be visible or not which affects if it is rendered
    # Not Yet Implemented
    def set_visibility(self, tile):
        tile.visible = True

    # Move the map around, takes a dx and dy from mouse movement event
    def move_map(self, dx, dy):
        # Loop through all tiles in the current zoom level only and move those
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            self.image_tiles[self.zoom_level]["tilesImages"][i - 1].move(dx, dy)
            # self.set_visibility(self.image_tiles[i - 1])

    # Requires the screen to display on
    # Displays all tiles of the current zoom_level with visibility set to true
    # Displays the tile at its screen_location variable
    def display(self, screen):
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            if self.image_tiles[self.zoom_level]["tilesImages"][i - 1].visible:
                screen.blit(self.image_tiles[self.zoom_level]["tilesImages"][i - 1].image,
                            self.image_tiles[self.zoom_level]["tilesImages"][i - 1].screen_location)

    # Accepts pixel x and y from the zoom_level coordinate system only
    # Returns a latitude and longitude
    def convert_pixels_to_degrees(self, zoom, pixelX, pixelY):
        # Converts to coordinate system determined by map density
        # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

        x = (pixelX / (256 * math.pow(2, zoom))) - 0.5
        y = 0.5 - (pixelY / (256 * math.pow(2, zoom)))

        lat = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
        lng = 360 * x

        return lat, lng

    # Accepts a latitude and longitude
    # Returns pixel coordinates in the zoom_level coordinate system
    def convert_degrees_to_pixels(self, zoom, lat, lng):
        # Converts to coordinate system determined by map density
        # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

        sinLatitude = math.sin(lat * math.pi / 180)

        x = (lng + 180) / 360
        y = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi))

        pixelX = int((x * 256 * math.pow(2, zoom)) + 0.5)
        pixelY = int((y * 256 * math.pow(2, zoom)) + 0.5)

        return pixelX, pixelY