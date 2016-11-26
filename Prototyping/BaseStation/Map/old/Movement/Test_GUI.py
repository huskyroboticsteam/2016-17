import pygame
import sys

pygame.init()
pygame.font.init()
from rover2 import *

# Set screen size
screenWidth = 1280
screenHeight = 720
screen = pygame.display.set_mode((screenWidth, screenHeight))

clock = pygame.time.Clock()
fps = 60
img = rover2("face", screen)

# This is only if the picture is incredibly large
# img.roverImage = pygame.transform.scale(img.roverImage, (screenWidth, screenHeight))
img.display(img.xAxis, img.yAxis)

xRel = 0
yRel = 0

while True:
    coord = pygame.mouse.get_pos()
    # Check if user is trying to close window
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            sys.exit()

        # This section is for rotating the image
        if (event.type == pygame.KEYDOWN):
            inputKey = event.key
            if (inputKey == pygame.K_RIGHT):
                angle = -90
            elif (inputKey == pygame.K_LEFT):
                angle = 90
            else:
                angle = 0

            oldRect = img.roverImage.get_rect(center=((screenWidth / 2 + img.xAxis), screenHeight / 2 + img.yAxis))
            img.roverImage, img.roverRect = img.rot_center(img.roverImage, oldRect, angle)
            screen.fill((0, 0, 0))
            img.rotateImage()

    if (pygame.mouse.get_pressed()[0]):
        coord = pygame.mouse.get_pos()
        img.moveMap(coord, xRel, yRel, screenWidth, screenHeight)
    else:
        xRel = coord[0] - img.xAxis
        yRel = coord[1] - img.yAxis

    screen.fill((0, 0, 0))
    img.display(img.xAxis, img.yAxis)
    pygame.display.flip()
    pygame.event.pump()