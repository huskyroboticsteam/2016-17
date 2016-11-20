import pygame
import urllib
import os
import math
import MapTile


class Map:
    def __init__(self):
        self.CENTER_COORDINATE = [39.346451, -112.586233]
        self.TILE_SIZE = [2000, 1500]
        self.STRAIGHT_LINE_APPROX = 111030  # m / degree
        # See: https://en.wikipedia.org/wiki/Geographic_coordinate_system for details

        self.tiles = 9
        self.zoom_level = 15

        self.image_tiles = []

    def retrieve_online_image(self, local_path, location, i):
        baseUrl = "http://dev.virtualearth.net/REST/V1/"
        callType = "Imagery/Map/AerialWithLabels/"
        apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"

        queryString = baseUrl + callType + location + apiKey
        print(queryString)

        if not os.path.exists(local_path):
            os.mkdir(local_path)

        urllib.urlretrieve(queryString, os.path.join(local_path, "map" + str(i) + ".jpg"))

    def retrieve_local_image(self, path, i):
        return pygame.image.load()

    def calculate_corner_center(self, lat, lng, tiles):
        tiles_to_corner = (math.sqrt(tiles) - 1) / 2

        # Get the center of the top left tile
        lat += (self.TILE_SIZE[1] * self.meterPerPixel / self.STRAIGHT_LINE_APPROX) * tiles_to_corner
        lng -= (self.TILE_SIZE[0] * self.meterPerPixel / self.STRAIGHT_LINE_APPROX) * tiles_to_corner

        return lat, lng

    def generate_single_map(self, zoom, lat, lng, tiles):

        zoom = int(zoom)
        lat = float(lat)
        lng = float(lng)
        tiles = int(tiles)

        self.meterPerPixel = 0;
        if zoom == 15:
            self.meterPerPixel = 4.78
        elif zoom == 16:
            self.meterPerPixel = 2.39
        elif zoom == 17:
            self.meterPerPixel = 1.19
        elif zoom == 18:
            self.meterPerPixel = 0.6
        else:
            self.meterPerPixel = 0.3

        lat, lng = self.calculate_corner_center(lat, lng, tiles)
        origLng = lng

        # 1 indexed loop so the math makes more sense
        for i in range(1, tiles + 1, 1):
            location = str(lat) + "," + str(lng) + "/" + str(zoom) + "?mapSize=" + str(self.TILE_SIZE[0]) + "," + \
                       str(self.TILE_SIZE[1])
            self.retrieve_online_image(str(zoom), location, i)
            # at the edge
            if i == int(math.sqrt(tiles)) or i == int(2 * math.sqrt(tiles)):
                lat -= 1500 * self.meterPerPixel / self.STRAIGHT_LINE_APPROX
                lng = origLng
            else:
                lng += 2000 * self.meterPerPixel / self.STRAIGHT_LINE_APPROX

    def generate_maps(self):
        zoom = raw_input("Select Zoom Level 15 - 19: ")
        lat = raw_input("Select Center Latitude: ")
        lng = raw_input("Select Center Longitude: ")
        tiles = raw_input("Number of Tiles (Square of Odds: 1, 9, 25): ")

        if zoom == "all":
           for i in range(15, 20):
               self.generate_single_map(i, lat, lng, tiles)
        else:
            self.generate_single_map(zoom, lat, lng, tiles)

    def zoom_in(self):
        if self.zoom_level < 19:
            self.zoom_level += 1
            self.image_tiles = []

    def zoom_out(self):
        if self.zoom_level > 15:
            self.zoom_level -= 1
            self.image_tiles = []

    def build_tiles(self):

            tiles_to_corner = (math.sqrt(self.tiles) - 1) / 2
            pixel = [-2000 * tiles_to_corner, -1500 * tiles_to_corner]

            for i in range(1, self.tiles + 1, 1):

                self.image_tiles.append(MapTile.MapTile(str(self.zoom_level), "map" + str(i) + ".jpg"))
                self.image_tiles[i - 1].screen_location = (pixel[0], pixel[1])

                # Decide whether or not the tile is initially on screen
                self.set_visibility(self.image_tiles[i - 1])

                if i == int(math.sqrt(self.tiles)) or i == int(2 * math.sqrt(self.tiles)):
                    pixel[0] = -2000 * tiles_to_corner
                    pixel[1] += 1500
                else:
                    pixel[0] += 2000

    def set_visibility(self, tile):
        return

    def move_map(self):
        for i in range(1, self.tiles + 1, 1):
            # Update locations here.
            self.set_visibility(self.image_tiles[i - 1])

    def display(self, screen):
        if len(self.image_tiles) == 0:
            self.build_tiles()

        for i in range(1, self.tiles + 1, 1):

            if self.image_tiles[i - 1].visible:
                screen.blit(self.image_tiles[i - 1].image, self.image_tiles[i - 1].screen_location)

    def convert_pixels_to_degrees(self):
        return

    def convert_degrees_to_pixels(self):
        return
