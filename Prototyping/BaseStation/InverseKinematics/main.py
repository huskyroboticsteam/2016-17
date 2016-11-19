import pygame
from pygame.locals import *
import numpy as np
from math import *

pygame.init()
screen = pygame.display.set_mode((640, 480))

running = 1


def to_vector(angle, length):
    return length * cos(angle), length * sin(angle)


class Arm:
    def __init__(self, length, angle_min, angle_max, after=None):
        self.length = length
        self.after = after  # The next limb
        self.angle_min = angle_min
        self.angle_max = angle_max

#    def parameters(self):
#        return [self.angle_rad] + [] if self.after is None else self.after.parameters()

    def draw(self, surface, position, angle, parameters):
        global_angle = angle + parameters[0]
        end = to_vector(global_angle, self.length) + position
        pygame.draw.line(surface, (0, 0, 0), position, end, 5)

        # Draw angle constraints
        pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(angle + self.angle_min, 30))
        pygame.draw.aaline(surface, (100, 0, 0), position, position + to_vector(angle + self.angle_max, 30))
        if self.after is not None:
            self.after.draw(surface, end, angle + parameters[0], parameters[1:])

    def error(self, target_pos, starting_pos, angle, parameters):
        end = to_vector(angle + parameters[0], self.length) + starting_pos
        if self.after is None:
            return np.linalg.norm(target_pos - end)
        else:
            return self.after.error(target_pos, end, angle + parameters[0], parameters[1:])

    def min_parameters(self):
        return [self.angle_min] + ([] if self.after is None else self.after.min_parameters())

    def max_parameters(self):
        return [self.angle_max] + ([] if self.after is None else self.after.max_parameters())

    def limb_count(self):
        return 1 if self.after is None else self.after.limb_count() + 1


def make_tentacle(segment_length, segment_count):
    if segment_count != 0:
        return Arm(segment_length, 0, 2 * pi, make_tentacle(segment_length, segment_count - 1))
    return None

base_position = np.array([320, 240])
# test_armature = make_tentacle(40, 10)
test_armature = Arm(50, -pi, 0, Arm(50, 0, pi / 3, Arm(30, 0, pi / 4, Arm(20, 0, 0))))

params = np.full(test_armature.limb_count(), 0)
target = np.array([0, 0])


def gradient_descent(armature, initial_parameters, base_pos, target_pos, iterations):
    parameters = np.copy(initial_parameters)
    parameters_min = armature.min_parameters()
    parameters_max = armature.max_parameters()
    parameter_step = np.full(len(parameters), .0001)
    delta = .0001

    for iter in xrange(iterations):
        base_error = armature.error(target_pos, base_pos, 0, parameters)

        # Calculate derivative for each axis
        derivative = np.empty(len(parameters))
        for i in xrange(len(parameters)):
            test_parameters = np.copy(parameters)
            test_parameters[i] += delta
            new_error = armature.error(target_pos, base_pos, 0, test_parameters)
            derivative[i] = (new_error - base_error) / delta

        # Step in the direction of the derivative to a given amount
        parameter_step *= .99
        parameters -= derivative * parameter_step

        parameters = np.clip(parameters, parameters_min, parameters_max)
    return parameters


def calculate_error():
    return test_armature.error(target, base_position, 0, params)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        if event.type == MOUSEMOTION:
            pass
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 3:
                pass

    if pygame.mouse.get_pressed()[2]:
        target = np.array(pygame.mouse.get_pos())
        params = gradient_descent(test_armature, params, base_position, target, 10)

    screen.fill((120, 120, 120))
    pygame.draw.circle(screen, (255, 20, 20), target, 10)
    test_armature.draw(screen, base_position, 0, params)
    pygame.display.flip()

pygame.quit()
