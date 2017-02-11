#! /usr/bin/env python2
import numpy as np
import transformations as tr

xaxis, yaxis, zaxis = np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])
pitch = yaxis
#yaw = zaxis
#roll = xaxis

def distance(end, target_pos):
    return np.linalg.norm(target_pos - end)


# A parameter with a min and a max
class Parameter:
    def __init__(self, min_angle, max_angle, axis=pitch):
        self.min = min_angle
        self.max = max_angle
        self.axis = axis

    def is_auto(self):
        return True
        
    def applyParameter(self, value, baseTransform):
        """Returns a new rotation matrix derived from the previous baseTransform
        with the given value of this parameter
        """
        return np.dot(baseTransform, tr.rotation_matrix(value, self.axis))

# A parameter with only one value, a joint fixed in global space
class StaticParameter(Parameter):
    def __init__(self, value):
        Parameter.__init__(self, value, value)

    def is_auto(self):
        return False
        
    def applyParameter(self, value, baseTransform):
        rx, ry, rz = tr.euler_from_matrix(baseTransform)
        return np.dot(baseTransform, tr.rotation_matrix(ry - self.min, self.axis))


# A parameter that is mechanically fixed, i.e. not used.
class FixedParameter(StaticParameter):
    def __init__(self, value):
        StaticParameter.__init__(self, value)


# A parameter with a min and a max and a setpoint
# Unused
class ManualParameter(Parameter):
    def __init__(self, min_angle, max_angle):
        Parameter.__init__(self, min_angle, max_angle)
        self.setpoint = min_angle

    def is_auto(self):
        return False


"""
An arm in three dimensions. Right now, only two angles of freedom are supported,
pitch and yaw. They should be passed in as some kind of Parameter.

Arm segements always exist along the positive x axis (forward)
Z is vertical
+Y is to the right

Pitch rotates around the Y axis
Roll rotates around the X axis
Yaw rotates around the Z 

The Arm class itself represents the structure of the arm, including segment lengths
and angle parameters. Most methods require a parameters list which holds information
regarding a specific configuration of the arm
"""
class Arm:
    def __init__(self, length, parameter, after=None):
        self.length = length
        self.after = after  # The next limb
        self.parameter = parameter

    def joints(self, parameters):
        """Returns the points representing the location of each joint in the arm
	    (convienant for drawing). You may have to do transformations on these points
	    to suit your graphical environment. One reccomendation is to intrepret the x
        and z coordinates as x and y (using something like point[::2])
        
        """
        return [np.zeros(3)] + self._joints_impl(tr.identity_matrix(), parameters)
	
    def _joints_impl(self, baseTransform, parameters):
        transform = self.applyTransform(parameters[0], baseTransform)
        end = tr.translation_from_matrix(transform)
		
        if self.after is not None:
            return [end] + self.after._joints_impl(transform, parameters[1:])
        else:
            return [end]

    def error(self, target_pos, baseTransform, parameters):
        transform = self.applyTransform(parameters[0], baseTransform)
        
        if self.after is None:
            end = tr.translation_from_matrix(transform)
            return distance(target_pos, end)
        else:
            return self.after.error(target_pos, transform, parameters[1:])
    
    #@cython.locals(armLength=np.ndarray, rPitch=np.ndarray, rYaw=np.ndarray, transform=np.ndarray)        
    def applyTransform(self, parameterValue, baseTransform):
        """Gives the translation matrix associated with this arm with the given pitch
        and yaw.
        
        """
        baseTransform = self.parameter.applyParameter(parameterValue, baseTransform)
        tLength = tr.translation_matrix(np.array([self.length, 0, 0]))
        
        return np.dot(baseTransform, tLength)        

    def min_parameters(self):
        return [self.parameter.min] + ([] if self.after is None else self.after.min_parameters())

    def max_parameters(self):
        return [self.parameter.max] + ([] if self.after is None else self.after.max_parameters())

    def limb_count(self):
        return 1 if self.after is None else self.after.limb_count() + 1

    def auto_parameters(self):
        return [self.parameter.is_auto()] + ([] if self.after is None else self.after.auto_parameters())


# def make_tentacle(segment_length, segment_count):
#     if segment_count != 0:
#         return Arm(segment_length, Parameter(-pi / 3, pi / 3, relative_angle),
#                    make_tentacle(segment_length * .9, segment_count - 1))
#     return None
