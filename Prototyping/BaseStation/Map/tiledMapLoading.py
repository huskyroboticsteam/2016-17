import pygame
from pygame.locals import *
import os
import sys
import urllib

# class constant
ZOOM_LEVEL = 15
CENTER_COORDINATE = [39.346451, -112.586233]
TILE_SIZE = [2000, 1500]

# know how many meter per pixel depending on the zoom level
meterPerPixel = 0;
if ZOOM_LEVEL == 15:
    meterPerPixel = 4.78
elif ZOOM_LEVEL == 16:
    meterPerPixel = 2.39
elif ZOOM_LEVEL == 17:
    meterPerPixel = 1.19
elif ZOOM_LEVEL == 18:
    meterPerPixel = 0.6
else:
    meterPerPixel = 0.3

screen = pygame.display.set_mode((1800, 1000))

baseUrl = "http://dev.virtualearth.net/REST/V1/"
callType = "Imagery/Map/AerialWithLabels/"
apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"


def getImage(location):
    queryString = baseUrl + callType + location + apiKey
    print(queryString)
    urllib.urlretrieve(queryString, os.path.join("data/", "map" + str(i) + ".jpg"))
    return pygame.image.load(os.path.join("data/", "map" + str(i) + ".jpg"))

# coordinates of each map
centerCoordinate = CENTER_COORDINATE
# store the image of each tile
newQuery = [0 for x in range(9)]

for i in range(0, 9, 1):
    sampleLocation = str(centerCoordinate[0]) + "," + str(centerCoordinate[1]) + "/" + str(ZOOM_LEVEL) + "?mapSize=" + \
                     str(TILE_SIZE[0]) + "," + str(TILE_SIZE[1])

    newQuery[i] = getImage(sampleLocation)
    # at the edge
    if i == 2 or i == 5:
        centerCoordinate[0] += 1500 * meterPerPixel / 111030
        centerCoordinate[1] += CENTER_COORDINATE[0]
        # print(centerCoordinate[0], centerCoordinate[1])
    else:
        centerCoordinate[1] += 2000 * meterPerPixel / 111030
        # print(centerCoordinate[0], centerCoordinate[1])

while True:
    # clock.tick(fps)
    coord = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))
    #top left corner of each image
    pixel = [0, 0]
    for i in range(0, 9, 1):
        screen.blit(newQuery[i], (pixel[0], pixel[1]))
        if i == 2 or i == 5:
            pixel[0] = 0
            pixel[1] += 1500
        else:
            pixel[0] += 2000
    pygame.display.flip()
    pygame.event.pump()