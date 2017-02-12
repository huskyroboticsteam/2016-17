"""
Filters average values of given inputs

Returns current gathered average when
filter() is called and given a value to
add to the average.

To Reset the average filter, use reset()
and supply new values in filter()

Written by Jaden Bottemiller in January 2017
EE Team of Husky Robotics
(Untested as of 2/7/2017)
"""


class AverageFilter(object):

    _sum = 0
    _num = 0

    def __init__(self):
        self._sum = 0
        self._num = 0

    def filter(self, input):
        self._num += 1
        self._sum += input
        return self._sum / self._num

    def reset(self):
        self._sum = 0
        self._num = 0
