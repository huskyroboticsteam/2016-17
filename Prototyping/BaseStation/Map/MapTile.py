import pygame
import os


class MapTile:
    def __init__(self, path, file_name, x, y):
        # Image dimensions will be static and handled by the map class

        self.image = pygame.image.load(os.path.join(path, file_name))
        # self.top_left = data.topl
        # self.bottom_right = data.bottomr
        # self.center = data.center

        # Top Left corner of the image
        self.screen_location = (x, y)

        # Whether the image is visible on screen
        self.visible = False

    def move(self, dx, dy):
        self.screen_location = (self.screen_location[0] + dx, self.screen_location[1] + dy)


