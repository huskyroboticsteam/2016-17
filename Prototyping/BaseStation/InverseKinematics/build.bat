@ECHO off
SET DISTUTILS_USE_SDK=1
SET MSSdk=1

python setup.py build_ext --inplace --compiler=msvc
