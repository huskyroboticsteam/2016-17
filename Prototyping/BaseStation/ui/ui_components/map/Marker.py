import pygame

class Marker:


    def __init__(self, x, y, centerX, centerY, screen, zoom_level, long, lat, rover):
        self.x = x
        self.y = y
        self.centerX = centerX
        self.centerY = centerY
        self.screen = screen
        self.zoom_level = zoom_level
        self.coordX = long
        self.coordY = lat
        self.rover = rover

    def draw(self):
        if self.rover:
            pygame.draw.circle(self.screen, (255, 0, 255), (int(self.x) - self.centerX, int(self.y) - self.centerY), 20)
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.x) - self.centerX, int(self.y) - self.centerY), 20)