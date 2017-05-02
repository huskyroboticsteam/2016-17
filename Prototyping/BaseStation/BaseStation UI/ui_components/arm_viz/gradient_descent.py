#! /usr/bin/env python2
import numpy as np
import transformations as tr
from armature import *

def gradient_descent(armature, initial_parameters, target_pos, iterations):
    parameters = np.array(initial_parameters, copy=True, dtype=np.float32)
    parameters_min = armature.min_parameters()
    parameters_max = armature.max_parameters()
    automatic_parameters = armature.auto_parameters()
    delta = .0001 # For calculating the derivative

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
        # Cap the size of the step
        parameter_step = min(base_error, 30) * .00005
        parameters -= derivative * parameter_step

        parameters = np.clip(parameters, parameters_min, parameters_max)
    return parameters
