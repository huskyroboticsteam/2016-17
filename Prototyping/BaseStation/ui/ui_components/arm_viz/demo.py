#! /usr/bin/env python2
"""
How to use the demo:
Left click and drag the target to set the target of the armature
Right click to adjust the wrist parameters
"""

import time
import pygame
from pygame.locals import *
import numpy as np
import transformations as tr
from armature import *
from math import pi
from gradient_descent import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
running = True
clock = pygame.time.Clock()

target_size = 10
moving_target = False

draw_origin = np.array([320, 0, 240])
draw_matrix = tr.translation_matrix(draw_origin)
# test_armature = make_tentacle(40, 10)
test_armature = Arm(50, Parameter(0, pi), FixedParameter(0),
                Arm(50, Parameter(0, pi), FixedParameter(0),
                Arm(30, Parameter(0, pi / 4), FixedParameter(0),
                Arm(10, Parameter(0, pi / 4), FixedParameter(0)))))

params = test_armature.min_parameters()
target = np.array([0, 0, 0])

while running:
    #clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:
                params[0] += event.rel[0] / 50
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                mouse_pos = np.array([pos[0], 0, pos[1]]) - draw_origin
                if distance(mouse_pos, target) < target_size:
                    moving_target = True
        elif event.type == MOUSEBUTTONUP:
            moving_target = False

    if moving_target:
        pos = pygame.mouse.get_pos()
        target = np.array([pos[0], 0, pos[1]]) - draw_origin

    #time_start = time.time()
    params = gradient_descent(test_armature, params, target, 10)
    #time_end = time.time()
    #print(time_end - time_start)

    screen.fill((120, 120, 120))
    pygame.draw.circle(screen, (255, 20, 20), (draw_origin + target)[::2], target_size)
    points = [point[::2] for point in test_armature.joints(params)]
    pygame.draw.lines(screen, (0,0,0), False, points + draw_origin[::2], 5)
    pygame.display.flip()

pygame.quit()
