import pygame

from pygame.locals import *

import os

import sys

import urllib

screen = pygame.display.set_mode((700, 300))

baseUrl = "http://dev.virtualearth.net/REST/V1/"

apiKey = "&key=AuAaQIpuk55T4X2UIhXfXitbUHHzIJNHlQLK-Y5v5Na_tx5cAz9Fvmw-xUR5oW8T"

callType = "Imagery/Map/Road/"

sampleLocation = "Bellevue%20Washington?mapLayer=TrafficFlow"

print(os.getcwd())


def getImage(location):
    queryString = baseUrl + callType + location + apiKey

    print(queryString)

    urllib.urlretrieve(queryString, "helloWorlds.jpg")

    # image1=Image.open("/Users/tanl/git/StaticMapsTesting2017/helloWorlds.png")

    image1 = pygame.image.load("helloWorlds.jpg")

    return image1


newQuery = getImage(sampleLocation)

while True:

    # clock.tick(fps)

    coord = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill((0, 0, 0))

    screen.blit(newQuery, (10, 10))

    pygame.display.flip()

    pygame.event.pump()
