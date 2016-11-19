import pygame
import os


class MapTile(pygame.image):
    def __init__(self, path, file_name, data):
        # Image dimensions will be static and handled by the map class

        self.load(os.path.join(path, file_name))
        self.top_left = data.topl
        self.bottom_right = data.bottomr
        self.center = data.center
