#! /usr/bin/env python3
import pygame
from pygame.locals import *
import numpy as np
from math import *
import transformations as tr

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
Yaw rotates around the Z axis
"""


def to_vector(angle, length):
    return length * cos(angle), length * sin(angle)


xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]


def distance(end, target_pos):
    return np.linalg.norm(target_pos - end)


# A parameter with a min and a max
class Parameter:
    def __init__(self, min_angle, max_angle):
        self.min = min_angle
        self.max = max_angle

    def max(self):
        return self.max

    def min(self):
        return self.min

    def is_auto(self):
        return True


# A parameter with only one value, a fixed joint
class StaticParameter(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, value, value)

    def is_auto(self):
        return False


# A parameter that is mechanically fixed, i.e. not used.
class FixedParameter(StaticParameter):
    def __init__(self, value):
        StaticParameter.__init__(self, value)


# A parameter with a min and a max and a setpoint
class ManualParameter(Parameter):
    def __init__(self, min_angle, max_angle):
        Parameter.__init__(self, min_angle, max_angle)
        self.setpoint = min_angle

    def setpoint(self):
        return self.setpoint

    def is_auto(self):
        return False


"""
An arm in three dimensions. Right now, only two angles of freedom are supported,
pitch and yaw. They should be passed in as some kind of Parameter
"""
class Arm:
    def __init__(self, length, pitch, yaw, after=None):
        self.length = length
        self.after = after  # The next limb
        self.pitch = pitch
        self.yaw = yaw

    def draw(self, surface, baseTransform, parameters):
        armLength = tr.translation_matrix([self.length, 0, 0])
        rPitch = tr.rotation_matrix(parameters[0], yaxis)
        rYaw = tr.rotation_matrix(parameters[1], zaxis)
        transform = tr.concatenate_matrices(baseTransform, rYaw, rPitch, armLength)

        start = tr.translation_from_matrix(baseTransform)
        end = tr.translation_from_matrix(transform)
        # Only use the y and z coords for a quick and dirty orthogonal projection
        pygame.draw.line(surface, (0, 0, 0), start[::2], end[::2], 5)

        # Draw angle constraints
        #pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(self.pitch.absolute_min(base_angle), 30))
        #pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(self.pitch.absolute_max(base_angle), 30))
        if self.after is not None:
            self.after.draw(surface, transform, parameters[2:])

    def error(self, target_pos, baseTransform, parameters):
        armLength = tr.translation_matrix([self.length, 0, 0])
        rPitch = tr.rotation_matrix(parameters[0], yaxis)
        rYaw = tr.rotation_matrix(parameters[1], zaxis)
        transform = tr.concatenate_matrices(baseTransform, rYaw, rPitch, armLength)

        if self.after is None:
            end = tr.translation_from_matrix(transform)
            return distance(target_pos, end)
        else:
            return self.after.error(target_pos, transform, parameters[2:])

    def min_parameters(self):
        return [self.pitch.min, self.yaw.min] + ([] if self.after is None else self.after.min_parameters())

    def max_parameters(self):
        return [self.pitch.max, self.yaw.max] + ([] if self.after is None else self.after.max_parameters())

    def limb_count(self):
        return 1 if self.after is None else self.after.limb_count() + 1

    def parameter_auto(self):
        return [self.pitch.is_auto(), self.yaw.is_auto()] + ([] if self.after is None else self.after.parameter_auto())


# def make_tentacle(segment_length, segment_count):
#     if segment_count != 0:
#         return Arm(segment_length, Parameter(-pi / 3, pi / 3, relative_angle),
#                    make_tentacle(segment_length * .9, segment_count - 1))
#     return None


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
                    Arm(30, Parameter(0, pi / 4), FixedParameter(0))))

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
