import math
import MapTile
import Utility
import pygame
import sys
import Marker


class Map:
    def __init__(self, map_name):
        self.markers = []
        self.coordinates = []
        # Size of all tiles for calculations
        self.TILE_SIZE = [1500, 1500]

        # Current map zoom and center
        self.zoom_level = 15
        self.center = (None, None)

        # Directory where map tiles are located
        self.folderName = None

        # Stores loaded in images
        self.image_tiles = {
            15: {
                "tiles": 1,
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
                "tiles": 9,
                "tilesImages": []
            },
            19: {
                "tiles": 9,
                "tilesImages": []
            }
        }

        self.open_map(map_name)

    def open_map(self, map_name):
        # Clear all map tiles
        for i in range(15, 20):
            self.image_tiles[i]["tilesImages"] = []

        self.parse_data_file(map_name)
        self.build_tiles()

    def zoom_in(self):
        if self.zoom_level < 19:
            self.adjust_map_for_zoom(pygame.mouse.get_pos(), self.zoom_level + 1)
            self.zoom_level += 1
            self.zoom_marker()

    def zoom_out(self):
        if self.zoom_level > 15:
            self.adjust_map_for_zoom(pygame.mouse.get_pos(), self.zoom_level - 1)
            self.zoom_level -= 1
            self.zoom_marker()

    def parse_data_file(self, name):

        # Open the file for reading
        f = open(name + ".dat", "r")
        dir = f.next().strip('\n')
        width = f.next().strip('\n')
        height = f.next().strip('\n')

        # Quit if the tile size specified in the map is different than what we are trying to load
        if int(width) != self.TILE_SIZE[0] or int(height) != self.TILE_SIZE[1]:
            print "Loading a map with incorrect tile size"
            print "Quitting..."
            sys.exit(1)

        lat = f.next().strip('\n')
        lng = f.next().strip('\n')
        f.close()

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
            pixel = [-self.TILE_SIZE[0] * tiles_to_corner, -self.TILE_SIZE[1] * tiles_to_corner]

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
                    pixel[0] = -self.TILE_SIZE[0] * tiles_to_corner
                    pixel[1] += self.TILE_SIZE[1]
                else:
                    pixel[0] += self.TILE_SIZE[0]

            out += "."
            print out

    # Chooses whether to set have the tile be visible or not which affects if it is rendered
    # Not Yet Implemented
    def set_visibility(self, tile):
        display_x = 1600
        display_y = 1100
        top_left_x = tile.screen_location[0]
        top_left_y = tile.screen_location[1]
        bottom_right_x = top_left_x + 2000
        bottom_right_y = top_left_y + 1500
        if bottom_right_x < 0 or bottom_right_y < 0:
            tile.visible = False
        elif top_left_x > display_x or top_left_y > display_y:
            tile.visible = False
        else:
            tile.visible = True

    # Move the map around, takes a dx and dy from mouse movement event
    def move_map(self, dx, dy):
        # Loop through all tiles in the current zoom level only and move those
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            self.image_tiles[self.zoom_level]["tilesImages"][i - 1].move(dx, dy)
            self.set_visibility(self.image_tiles[self.zoom_level]["tilesImages"][i - 1])
        for marker in self.markers:
            marker.x = marker.x + dx
            marker.y = marker.y + dy

    # Requires the screen to display on
    # Displays all tiles of the current zoom_level with visibility set to true
    # Displays the tile at its screen_location variable
    def display(self, screen):
        self.screen = screen
        for i in range(1, self.image_tiles[self.zoom_level]["tiles"] + 1, 1):
            if self.image_tiles[self.zoom_level]["tilesImages"][i - 1].visible:
                screen.blit(self.image_tiles[self.zoom_level]["tilesImages"][i - 1].image,
                            self.image_tiles[self.zoom_level]["tilesImages"][i - 1].screen_location)
        self.draw_marker()

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
    def get_mouse_lat_lng(self, mouse_pos):
        x, y = self.get_mouse_pos_projection(mouse_pos)
        lat, lng = Utility.convert_pixels_to_degrees(self.zoom_level, x, y)
        print lat, lng
        return lat, lng

    def adjust_map_for_zoom(self, mouse_pos, zoom):

        target_x = mouse_pos[0]
        target_y = mouse_pos[1]

        # Get mouse position in latitude and longitude
        lat, lng = self.get_mouse_lat_lng(mouse_pos)

        # Get the mouse click position on the Bing Coordinate System
        pixelX, pixelY = Utility.convert_degrees_to_pixels(zoom, lat, lng)

        # Get the center of the map in the Bing Coordinate System
        centerX, centerY = Utility.convert_degrees_to_pixels(zoom, self.center[0], self.center[1])

        # Get the pixel position of the top left corner of the center tile on the Bing Coordinate System
        centerX -= self.TILE_SIZE[0] / 2
        centerY -= self.TILE_SIZE[1] / 2

        # Get the vector from the top left of center tile (know position of) to the point we want to move
        dx = pixelX - centerX
        dy = pixelY - centerY

        # The position of the top left corner of the center tile of the map
        center = self.image_tiles[zoom]["tilesImages"][((self.image_tiles[zoom]["tiles"] + 1) / 2) - 1]
        center_location = center.screen_location

        # The position of the point that we want to be at the mouse click position
        x = center_location[0] + dx
        y = center_location[1] + dy

        # Get the components of the vector from the current point to the destination
        dx = target_x - x
        dy = target_y - y

        # Adjust all tiles by the target vector
        for i in range(0, len(self.image_tiles[zoom]["tilesImages"])):
            self.image_tiles[zoom]["tilesImages"][i].move(dx, dy)

    # add the position of the rover giving x and y coordinates
    def add_rover(self, x, y):
        self.add_marker(x, y, True)

    # add a new marker given the specified coordinates x and y, assuming that this isn't a rover
    def add_marker(self, x, y):
        # generates a new marker object
        self.add_marker(x, y, False)

    # draw every marker on the screen
    def draw_marker(self):
        for marker in self.markers:
            marker.draw()

    # changes the position of markers after zooming in
    def zoom_marker(self):
        new_marker = []
        for marker in self.markers:
            new_marker.append(self.make_marker(marker.coordX, marker.coordY, marker.rover))

        self.markers = new_marker

    # creates a new marker object with the given coordinate x and y
    def make_marker(self, x, y, rover):
        pixelCoord = Utility.convert_degrees_to_pixels(self.zoom_level, x, y)
        self.centerX2, self.centerY2 = Utility.convert_degrees_to_pixels(self.zoom_level, self.center[0],
                                                                         self.center[1])
        center = self.image_tiles[self.zoom_level]["tilesImages"][
            ((self.image_tiles[self.zoom_level]["tiles"] + 1) / 2) - 1]
        self.center_location = center.screen_location

        self.centerX2 -= self.TILE_SIZE[0] / 2
        self.centerY2 -= self.TILE_SIZE[1] / 2

        return Marker.Marker(pixelCoord[0] + self.center_location[0], pixelCoord[1] + self.center_location[1],
                          self.centerX2, self.centerY2, self.screen, self.zoom_level, x, y, rover)

