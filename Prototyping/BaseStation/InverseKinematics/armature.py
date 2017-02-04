#! /usr/bin/env python2
import numpy as np
import transformations as tr

xaxis, yaxis, zaxis = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])

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

    def joints(self, parameters):
        """Returns the points representing the location of each joint in the arm
	    (convienant for drawing). You may have to do transformations on these points
	    to suit your graphical environment. The points will be in a projected 2d space
        
        """
        return [np.zeros(2)] + self._joints_impl(tr.identity_matrix(), parameters)
		
    def _joints_impl(self, baseTransform, parameters):
        armLength = tr.translation_matrix(np.array([self.length, 0, 0]))
        rPitch = tr.rotation_matrix(parameters[0], yaxis)
        rYaw = tr.rotation_matrix(parameters[1], zaxis)
        
        transform = tr.concatenate_matrices([baseTransform, rYaw, rPitch, armLength])
        #transform = armLength * rPitch * rYaw * baseTransform
        #transform = baseTransform * rYaw * rPitch * armLength

        # Only use the y and z coords for a quick and dirty orthogonal projection
        end = tr.translation_from_matrix(transform)[::2]
		
        if self.after is not None:
            return [end] + self.after._joints_impl(transform, parameters[2:])
        else:
            return [end]

    def error(self, target_pos, baseTransform, parameters):
        armLength = tr.translation_matrix(np.array([self.length, 0, 0]))
        rPitch = tr.rotation_matrix(parameters[0], yaxis)
        rYaw = tr.rotation_matrix(parameters[1], zaxis)
		
        transform = tr.concatenate_matrices([baseTransform, rYaw, rPitch, armLength])
        #transform = armLength * rPitch * rYaw * baseTransform
        #transform = baseTransform * rYaw * rPitch * armLength

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
