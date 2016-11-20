import pygame
import os


class MapTile:
    def __init__(self, path, file_name):
        # Image dimensions will be static and handled by the map class

        self.image = pygame.image.load(os.path.join(path, file_name))
        # self.top_left = data.topl
        # self.bottom_right = data.bottomr
        # self.center = data.center

        # Top Left corner of the image
        self.screen_location = None
        self.visible = False


