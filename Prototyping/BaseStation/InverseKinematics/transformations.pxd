cimport numpy

__version__ = '2015.07.18'
__docformat__ = 'restructuredtext en'
__all__ = ()

DTYPE = numpy.float32
ctypedef numpy.float32_t DTYPE_t

cpdef numpy.ndarray identity_matrix()
cpdef numpy.ndarray translation_matrix(numpy.ndarray direction)
cpdef numpy.ndarray translation_from_matrix(numpy.ndarray matrix)
#cpdef numpy.ndarray, numpy.ndarray reflection_from_matrix(matrix)
cpdef numpy.ndarray rotation_matrix(float angle, numpy.ndarray direction, numpy.ndarray point=*)
cpdef numpy.ndarray rotation_from_matrix(numpy.ndarray matrix)
cpdef numpy.ndarray scale_matrix(float factor, numpy.ndarray origin=*, numpy.ndarray direction=*)
cpdef numpy.ndarray scale_from_matrix(numpy.ndarray matrix)
cpdef numpy.ndarray projection_matrix(numpy.ndarray point, numpy.ndarray normal, numpy.ndarray direction=*, numpy.ndarray perspective=*, bint pseudo=*)
cpdef numpy.ndarray projection_from_matrix(numpy.ndarray matrix, bint pseudo=*)
cpdef numpy.ndarray clip_matrix(float left, float right, float bottom, float top, float near, float far, numpy.ndarray perspective=*)
cpdef numpy.ndarray shear_matrix(float angle, numpy.ndarray direction, numpy.ndarray point, numpy.ndarray normal)
cpdef numpy.ndarray shear_from_matrix(numpy.ndarray matrix)
#def numpy.ndarray decompose_matrix(matrix)
cpdef numpy.ndarray compose_matrix(numpy.ndarray scale=*, shear=*, numpy.ndarray angles=*, numpy.ndarray translate=*, numpy.ndarray perspective=*)
#def numpy.ndarray orthogonalization_matrix(lengths, angles)
#def numpy.ndarray affine_matrix_from_points(v0, v1, shear=True, scale=True, usesvd=True)
#def numpy.ndarray superimposition_matrix(v0, v1, scale=False, usesvd=True)
#def numpy.ndarray euler_matrix(ai, aj, ak, axes='sxyz')
#def numpy.ndarray euler_from_matrix(matrix, axes='sxyz')
#def euler_from_quaternion(quaternion, axes='sxyz')
#def quaternion_from_euler(ai, aj, ak, axes='sxyz')
#def quaternion_about_axis(angle, axis)
#def quaternion_matrix(quaternion)
#def quaternion_from_matrix(matrix, isprecise=False)
#def quaternion_multiply(quaternion1, quaternion0)
#def quaternion_conjugate(quaternion)
#def quaternion_inverse(quaternion)
#def quaternion_real(quaternion)
#def quaternion_imag(quaternion)
#def quaternion_slerp(quat0, quat1, fraction, spin=0, shortestpath=True)
#def random_quaternion(rand=None)
#def random_rotation_matrix(rand=None)

#class Arcball(object):
#    def __init__(self, initial=None)
#    def place(self, center, radius)
#    def setaxes(self, *axes)
#    def constrain(self)
#    def constrain(self, value)
#    def down(self, point)
#    def drag(self, point)
#	def next(self, acceleration=0.0)
#	def matrix(self)
#	
#def arcball_map_to_sphere(point, center, radius)
#def arcball_constrain_to_axis(point, axis)
#def arcball_nearest_axis(point, axes)

# epsilon for testing whether a number is close to zero
#_EPS = numpy.finfo(float).eps * 4.0

# axis sequences for Euler angles
#_NEXT_AXIS = [1, 2, 0, 1]

# map axes strings to/from tuples of inner axis, parity, repetition, frame
#_AXES2TUPLE = {
#    'sxyz': (0, 0, 0, 0), 'sxyx': (0, 0, 1, 0), 'sxzy': (0, 1, 0, 0),
#    'sxzx': (0, 1, 1, 0), 'syzx': (1, 0, 0, 0), 'syzy': (1, 0, 1, 0),
#    'syxz': (1, 1, 0, 0), 'syxy': (1, 1, 1, 0), 'szxy': (2, 0, 0, 0),
#    'szxz': (2, 0, 1, 0), 'szyx': (2, 1, 0, 0), 'szyz': (2, 1, 1, 0),
#    'rzyx': (0, 0, 0, 1), 'rxyx': (0, 0, 1, 1), 'ryzx': (0, 1, 0, 1),
#    'rxzx': (0, 1, 1, 1), 'rxzy': (1, 0, 0, 1), 'ryzy': (1, 0, 1, 1),
#    'rzxy': (1, 1, 0, 1), 'ryxy': (1, 1, 1, 1), 'ryxz': (2, 0, 0, 1),
#    'rzxz': (2, 0, 1, 1), 'rxyz': (2, 1, 0, 1), 'rzyz': (2, 1, 1, 1)}

#_TUPLE2AXES = dict((v, k) for k, v in _AXES2TUPLE.items())

cpdef numpy.ndarray vector_norm(numpy.ndarray data, numpy.ndarray axis=*, numpy.ndarray out=*)
cpdef numpy.ndarray unit_vector(numpy.ndarray data, numpy.ndarray axis=*, numpy.ndarray out=*)
cpdef numpy.ndarray random_vector(int size)
cpdef numpy.ndarray vector_product(numpy.ndarray v0, numpy.ndarray v1, int axis=*)
cpdef numpy.ndarray angle_between_vectors(numpy.ndarray v0, numpy.ndarray v1, bint directed=*, int axis=*)
cpdef numpy.ndarray inverse_matrix(numpy.ndarray matrix)
#cpdef numpy.ndarray concatenate_matrices(numpy.ndarray matrices)
cpdef bint is_same_transform(numpy.ndarray matrix0, numpy.ndarray matrix1)
