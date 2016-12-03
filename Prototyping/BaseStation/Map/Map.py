import urllib
import os
import math
import MapTile


class Map:
    def __init__(self):
        self.TILE_SIZE = [2000, 1500]

        self.zoom_level = 15

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

    def retrieve_online_image(self, local_path, location, i):
        baseUrl = "http://dev.virtualearth.net/REST/V1/"
        callType = "Imagery/Map/AerialWithLabels/"
        apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"

        queryString = baseUrl + callType + location + apiKey
        print(queryString)

        if not os.path.exists(local_path):
            os.mkdir(local_path)

        urllib.urlretrieve(queryString, os.path.join(local_path, "map" + str(i) + ".jpg"))

    def calculate_corner_center(self, zoom, lat, lng, tiles):
        tiles_to_corner = (math.sqrt(tiles) - 1) / 2

        x, y = self.convert_degrees_to_pixels(zoom, lat, lng)
        x -= tiles_to_corner * 2000
        y -= tiles_to_corner * 1500

        return x, y

    def generate_single_map(self, zoom, lat, lng, tiles):

        zoom = int(zoom)
        lat = float(lat)
        lng = float(lng)
        tiles = int(tiles)

        x, y = self.calculate_corner_center(zoom, lat, lng, tiles)
        originalX = x

        # 1 indexed loop so the math makes more sense
        for i in range(1, tiles + 1, 1):
            lat, lng = self.convert_pixels_to_degrees(zoom, x, y)
            location = str(lat) + "," + str(lng) + "/" + str(zoom) + "?mapSize=" + str(self.TILE_SIZE[0]) + "," + \
                       str(self.TILE_SIZE[1])
            self.retrieve_online_image(str(zoom), location, i)
            # at the edge
            if i % math.sqrt(self.image_tiles[zoom]["tiles"]) == 0:
                y += 1500
                x = originalX
            else:
                x += 2000

    def generate_maps(self):
        zoom = raw_input("Select Zoom Level 15 - 19: ")
        lat = raw_input("Select Center Latitude: ")
        lng = raw_input("Select Center Longitude: ")

        if zoom == "all":
            for i in range(15, 20):
                if i < 18:
                    self.generate_single_map(i, lat, lng, 9)
                else:
                    self.generate_single_map(i, lat, lng, 25)
        else:
            if zoom < 18:
                self.generate_single_map(zoom, lat, lng, 9)
            else:
                self.generate_single_map(zoom, lat, lng, 25)

    def zoom_in(self):
        if self.zoom_level < 19:
            self.zoom_level += 1

    def zoom_out(self):
        if self.zoom_level > 15:
            self.zoom_level -= 1

    def build_tiles(self):
            for i in range(15, 20, 1):

                tiles_to_corner = (math.sqrt(self.image_tiles[i]["tiles"]) - 1) / 2
                pixel = [-2000 * tiles_to_corner, -1500 * tiles_to_corner]

                for j in range(1, self.image_tiles[i]["tiles"] + 1, 1):

                    self.image_tiles[i]["tilesImages"].append(MapTile.MapTile(str(i), "map" + str(j) + ".jpg", pixel[0], pixel[1]))

                    # Decide whether or not the tile is initially on screen
                    self.set_visibility(self.image_tiles[i]["tilesImages"][j - 1])

                    if j % math.sqrt(self.image_tiles[i]["tiles"]) == 0:
                        pixel[0] = -2000 * tiles_to_corner
                        pixel[1] += 1500
                    else:
                        pixel[0] += 2000

    def set_visibility(self, tile):
        tile.visible = True

    def move_map(self, dx, dy):
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            self.image_tiles[self.zoom_level]["tilesImages"][i - 1].move(dx, dy)
            # self.set_visibility(self.image_tiles[i - 1])

    def display(self, screen):
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            if self.image_tiles[self.zoom_level]["tilesImages"][i - 1].visible:
                screen.blit(self.image_tiles[self.zoom_level]["tilesImages"][i - 1].image, self.image_tiles[self.zoom_level]["tilesImages"][i - 1].screen_location)

    # Accepts pixel x and y from the zoom_level coordinate system only
    def convert_pixels_to_degrees(self, zoom, pixelX, pixelY):
        # Converts to coordinate system determined by map density
        # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

        x = (pixelX / (256 * math.pow(2, zoom))) - 0.5
        y = 0.5 - (pixelY / (256 * math.pow(2, zoom)))

        lat = 90 - 360 * math.atan(math.exp(-y * 2 * math.pi)) / math.pi
        lng = 360 * x

        return lat, lng

    # Converts lat and lng to pixels in the zoom level grid
    def convert_degrees_to_pixels(self, zoom, lat, lng):
        # Converts to coordinate system determined by map density
        # See https://msdn.microsoft.com/en-us/library/bb259689.aspx for details

        sinLatitude = math.sin(lat * math.pi / 180)

        x = (lng + 180) / 360
        y = (0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / (4 * math.pi))

        pixelX = int((x * 256 * math.pow(2, zoom)) + 0.5)
        pixelY = int((y * 256 * math.pow(2, zoom)) + 0.5)

        return pixelX, pixelY

    def printStuff(self):
        print self.image_tiles
