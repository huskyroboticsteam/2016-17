# Inspired by https://p5js.org/examples/interaction-reach-2.html

import pygame
from pygame.locals import *
from math import *
import numpy as np

width = 640
height = 480

pygame.init()
screen = pygame.display.set_mode((width, height))

running = 1

numSegments = 3
x = [0] * numSegments
y = [0] * numSegments
angle = [0] * numSegments

# Base coordinate
x[-1] = width / 2
y[-1] = height / 2

segLength = [50, 70, 30]

targetX = 0
targetY = 0


def reachSegment(i, xin, yin):
    global targetX, targetY
    dx = xin - x[i]
    dy = yin - y[i]
    angle[i] = atan2(dy, dx)
    targetX = xin - cos(angle[i]) * segLength[i]
    targetY = yin - sin(angle[i]) * segLength[i]


def positionSegment(a, b):
    x[b] = x[a] + cos(angle[a]) * segLength[i]
    y[b] = y[a] + sin(angle[a]) * segLength[i]

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0

    screen.fill((120, 120, 120))

    mouseX, mouseY = pygame.mouse.get_pos()
    reachSegment(0, mouseX, mouseY)
    for i in xrange(1, numSegments):
        reachSegment(i, targetX, targetY)
    for i in xrange(len(x) - 1, 0, -1):
        positionSegment(i, i-1)
    for i in xrange(len(x)):
        pygame.draw.circle(screen, (0, 200, 0), (int(x[i]), int(y[i])), 4)
        pygame.draw.line(screen, (i * 40, i * 40, i * 40), (x[i], y[i]), (x[i] + segLength[i] * cos(angle[i]),
                                                           y[i] + segLength[i] * sin(angle[i])), 5)

    endpoint = np.array([x[0] + segLength[0] * cos(angle[0]), y[0] + segLength[0] * sin(angle[0])])
    mouse = np.array(pygame.mouse.get_pos())
    print np.linalg.norm(endpoint - mouse)

    # pygame.time.wait(1000)
    pygame.display.flip()

pygame.quit()
