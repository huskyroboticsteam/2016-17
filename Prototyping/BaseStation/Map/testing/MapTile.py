import pygame
import os


class MapTile:
    def __init__(self, path, file_name, x, y):
        # Image dimensions will be static and handled by the map class

        # Image for the tile
        self.image = pygame.image.load(os.path.join(path, file_name))

        # Top left corner of the image
        self.screen_location = (x, y)

        # Whether the image is visible on screen
        self.visible = False

    # Update the location on screen when moving
    def move(self, dx, dy):
        self.screen_location = (self.screen_location[0] + dx, self.screen_location[1] + dy)