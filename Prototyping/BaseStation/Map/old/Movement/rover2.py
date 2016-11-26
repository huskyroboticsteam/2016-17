import pygame
import sys

class rover2:

    roverImage = pygame.image.load("../15/map1.jpg")
    roverRect = roverImage.get_rect()

    def __init__(self, name, screen):
        self.name = name
        self.screen = screen
        self.xAxis = 0
        self.yAxis = 0

    def display(self, x, y):
        self.screen.blit(self.roverImage, (x,y))

    # This is only used for rotating the image
    def rotateImage(self):
        self.screen.blit(self.roverImage, self.roverRect)

    def moveMap(self, mouseCoord, xRelevant, yRelevant, screenWidth, screenHeight):
        if (mouseCoord[0] >= screenWidth):
            self.xAxis = screenWidth
        elif (mouseCoord[0] < screenWidth):
            self.xAxis = mouseCoord[0] - xRelevant
        if (mouseCoord[1] >= screenHeight):
            self.yAxis = screenHeight
        elif (mouseCoord[1] < screenHeight):
            self.yAxis = mouseCoord[1] - yRelevant

    # For rotating image only
    def rot_center(self, image, rect, angle):
        #rotate an image while keeping its center
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect