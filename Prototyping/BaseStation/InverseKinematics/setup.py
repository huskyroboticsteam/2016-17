# https://github.com/cython/cython/wiki/CythonExtensionsOnWindows
# http://docs.cython.org/src/reference/compilation.html

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Build import cythonize
import numpy

setup(
	#name="InverseKinematics",
	ext_modules = cythonize(["gradient_descent.py", "armature.py", "transformations.py"]),
	include_dirs=[numpy.get_include(), "."]
    #package_dir={'cython_test': ''}
)
