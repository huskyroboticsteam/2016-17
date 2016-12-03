#! /usr/bin/env python3
import pygame
from pygame.locals import *
import numpy as np
from math import *

"""
How to use the demo:
Left click to set the target of the armature
Right click to adjust the wrist parameters

must be run directly, or call main() to start
"""


def to_vector(angle, length):
    return length * cos(angle), length * sin(angle)


def relative_angle(base_angle, parameter):
    return base_angle + parameter


def absolute_angle(base_angle, parameter):
    return parameter


# A parameter with a min and a max
class Parameter:
    def __init__(self, min_angle, max_angle, absolute_calculator):
        self.min = min_angle
        self.max = max_angle
        self.absolute_calculator = absolute_calculator

    def absolute_max(self, base_angle):
        return self.absolute_angle(base_angle, self.max)

    def absolute_min(self, base_angle):
        return self.absolute_angle(base_angle, self.min)

    def absolute_angle(self, base_angle, parameter_angle):
        return self.absolute_calculator(base_angle, parameter_angle)

    def is_manual(self):
        return False


# A parameter with a min and a max and a setpoint
class ManualParameter(Parameter):
    def __init__(self, min_angle, max_angle, absolute_calculator):
        Parameter.__init__(self, min_angle, max_angle, absolute_calculator)
        self.setponit = min_angle

    def absolute_setpoint(self, base_angle):
        return self.absolute_angle(base_angle, self.setponit)

    def is_manual(self):
        return True


class Arm:
    def __init__(self, length, angle, after=None):
        self.length = length
        self.after = after  # The next limb
        self.angle = angle

    def draw(self, surface, position, base_angle, parameters):
        global_angle = self.angle.absolute_angle(base_angle, parameters[0])
        end = to_vector(global_angle, self.length) + position
        pygame.draw.line(surface, (0, 0, 0), position, end, 5)

        # Draw angle constraints
        pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(self.angle.absolute_min(base_angle), 30))
        pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(self.angle.absolute_max(base_angle), 30))
        if self.after is not None:
            self.after.draw(surface, end, global_angle, parameters[1:])

    def error(self, target_pos, starting_pos, base_angle, parameters):
        global_angle = self.angle.absolute_angle(base_angle, parameters[0])
        end = to_vector(global_angle, self.length) + starting_pos
        if self.after is None:
            return np.linalg.norm(target_pos - end)
        else:
            return self.after.error(target_pos, end, global_angle, parameters[1:])

    def min_parameters(self):
        return [self.angle.min] + ([] if self.after is None else self.after.min_parameters())

    def max_parameters(self):
        return [self.angle.max] + ([] if self.after is None else self.after.max_parameters())

    def limb_count(self):
        return 1 if self.after is None else self.after.limb_count() + 1

    def parameter_manual(self):
        return [self.angle.is_manual()] + ([] if self.after is None else self.after.parameter_manual())


def make_tentacle(segment_length, segment_count):
    if segment_count != 0:
        return Arm(segment_length, Parameter(-pi / 3, pi / 3, relative_angle),
                   make_tentacle(segment_length * .9, segment_count - 1))
    return None


def gradient_descent(armature, initial_parameters, manual_parameters, base_pos, target_pos, iterations):
    parameters = np.copy(initial_parameters)
    parameters_min = armature.min_parameters()
    parameters_max = armature.max_parameters()
    parameter_step = np.full(len(parameters), .0001)
    delta = .0001

    for iter in range(iterations):
        base_error = armature.error(target_pos, base_pos, 0, parameters)

        # Calculate derivative for each axis
        derivative = np.empty(len(parameters))
        for i in range(len(parameters)):
            if manual_parameters[i]:
                derivative[i] = 0
            else:
                test_parameters = np.copy(parameters)
                test_parameters[i] += delta
                new_error = armature.error(target_pos, base_pos, 0, test_parameters)
                derivative[i] = (new_error - base_error) / delta

        # Step in the direction of the derivative to a given amount
        parameter_step *= .99
        parameters -= derivative * parameter_step

        parameters = np.clip(parameters, parameters_min, parameters_max)
    return parameters


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    running = True
    clock = pygame.time.Clock()

    base_position = np.array([320, 240])
    # test_armature = make_tentacle(40, 10)
    test_armature = Arm(50, Parameter(-pi, 0, relative_angle),
                        Arm(50, Parameter(0, pi, relative_angle),
                            Arm(30, Parameter(0, pi / 4, relative_angle),
                                Arm(20, ManualParameter(-pi / 4, pi / 4, absolute_angle)))))

    params = np.full(test_armature.limb_count(), 0)
    params_manual = test_armature.parameter_manual()
    target = np.array([0, 0])

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            if event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[2]:
                    params[3] += event.rel[0] / 50
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    pass

        if pygame.mouse.get_pressed()[0]:
            target = np.array(pygame.mouse.get_pos())

        params = gradient_descent(test_armature, params, params_manual, base_position, target, 100)

        screen.fill((120, 120, 120))
        pygame.draw.circle(screen, (255, 20, 20), target, 10)
        test_armature.draw(screen, base_position, 0, params)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
