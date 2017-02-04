import pygame

class Marker:
    def __init__(self, x, y, centerX, centerY, screen, zoom_level):
        self.x = x
        self.y = y
        self.centerX = centerX
        self.centerY = centerY
        self.screen = screen
        self.zoom_level = zoom_level

    def draw(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x) - self.centerX, int(self.y) - self.centerY), 20)