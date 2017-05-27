#!/usr/bin/env python
from math import *
import arm_hardware as hw
import time

print "Press Cal"

for i in xrange(600):
    value = sin((pi * i) / 100.0)
    if i % 10 == 0:
        print str(value)
    hw.motors[0].write(value)
    time.sleep(.02)

hw.motors[0].write(0)
print "Release CAL"
time.sleep(20)