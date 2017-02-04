#! /usr/bin/env python2
import pygame
from pygame.locals import *
import numpy as np
from math import *
import transformations as tr
from armature import *

"""
How to use the demo:
Left click and drag the target to set the target of the armature
Right click to adjust the wrist parameters

must be run directly, or call main() to start


Arm segements always exist along the positive x axis (forward)
Z is vertical
+Y is to the right

Pitch rotates around the Y axis
Roll rotates around the X axis
Yaw rotates around the Z 
"""


def gradient_descent(armature, initial_parameters, automatic_parameters, target_pos, iterations):
    parameters = np.copy(initial_parameters)
    parameters_min = armature.min_parameters()
    parameters_max = armature.max_parameters()
    parameter_step = np.full(len(parameters), .0005)
    delta = .0001

    tBase = tr.identity_matrix()

    for iter in range(iterations):
        base_error = armature.error(target_pos, tBase, parameters)

        # Calculate derivative for each axis
        derivative = np.empty(len(parameters))
        for i in range(len(parameters)):
            if automatic_parameters[i]:
                test_parameters = np.copy(parameters)
                test_parameters[i] += delta
                new_error = armature.error(target_pos, tBase, test_parameters)
                derivative[i] = (new_error - base_error) / delta
            else:
                derivative[i] = 0

        # Step in the direction of the derivative to a given amount
        parameter_step *= .9
        parameters -= derivative * parameter_step

        parameters = np.clip(parameters, parameters_min, parameters_max)
    return parameters


def main():
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

    params = np.full(test_armature.limb_count() * 2, 0)
    params_auto = test_armature.parameter_auto()
    target = np.array([0, 0, 0])

    while running:
        clock.tick(60)
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

        params = gradient_descent(test_armature, params, params_auto, target, 50)

        screen.fill((120, 120, 120))
        pygame.draw.circle(screen, (255, 20, 20), (draw_origin + target)[::2], target_size)
        test_armature.draw(screen, draw_matrix, params)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
