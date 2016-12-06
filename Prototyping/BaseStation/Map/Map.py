import math
import MapTile
import Utility
import Generator
import os


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

        self.open_map()

    def open_map(self):
        # Clear all map tiles
        for i in range(15, 20):
            self.image_tiles[i]["tilesImages"] = []

        # Decides whether to generate a new map
        new = raw_input("Generate New Map (Y/N): ")

        if new == "Y" or new == "y":
            g = Generator.Generator(self.TILE_SIZE, self.image_tiles)
            name = g.generate_maps()
            self.parse_data_file(name)
        else:
            while True:
                name = raw_input("Map Name? ")
                if os.path.exists(name):
                    break
                else:
                    print "Map doesn't exist"

            self.parse_data_file(name)

        self.build_tiles()

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

        print "Map Location: " + dir
        print "Center of Map: " + lat + ", " + lng

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

    def get_real_mouse_screen_pos(self, mouse):

        # The position of the mouse in the screen coordinate system
        screen_x = mouse[0]
        screen_y = mouse[1]

        # The position of the top left corner of the center tile of the map
        center = self.image_tiles[self.zoom_level]["tilesImages"][((self.image_tiles[self.zoom_level]["tiles"] + 1) / 2) - 1]
        center_location = center.screen_location

        # The mouse position adjusted for map movements
        x = screen_x - center_location[0]
        y = screen_y - center_location[1]

        return x, y

    def get_mouse_pos_projection(self, mouse):

        # Get mouse position adjusted for map movements
        x, y = self.get_real_mouse_screen_pos(mouse)

        # Get the center of the map in the Bing Coordinate System
        center_bing_x, center_bing_y = Utility.convert_degrees_to_pixels(self.zoom_level, self.center[0], self.center[1])

        # Get the pixel position of the top left corner of the center tile on the Bing Coordinate System
        center_bing_x -= self.TILE_SIZE[0] / 2
        center_bing_y -= self.TILE_SIZE[1] / 2

        # Get the position in the Bing Coordinate System of the mouse
        current_bing_x = center_bing_x + x
        current_bing_y = center_bing_y + y

        return current_bing_x, current_bing_y

    # Converts mouse position in the Bing Coordinate System to latitude and longitude
    def get_mouse_lat_lng(self, mouse):
        x, y = self.get_mouse_pos_projection(mouse)
        lat, lng = Utility.convert_pixels_to_degrees(self.zoom_level, x, y)
        print lat, lng
        return lat, lng
