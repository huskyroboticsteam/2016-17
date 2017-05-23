#!/usr/bin/env python
from math import *
from sabertooth import *
import atexit
import arm_hardware as hw

if __name__ == "__main__":
    import argparse
    from timedeltatype import *
    import time 

    def float_range(min, max):
        def float_test(x):
            x = float(x)
            if x < min or x > max:
                raise argparse.ArgumentTypeError("%r not in range [%.1f, %.1f]"%(x,min,max))
            return x
        return float_test
    
    def set_motors(motors, value):
        for motor in motors:
            motor.write(value)
        
    parser = argparse.ArgumentParser(description='Arm control script')
    parser.add_argument('strength', type=float_range(-1,1), help='Strength as a value between -1 and 1. -1 is reverse')
    parser.add_argument('joints', choices=hw.jointNames, help='The joint to control.', nargs='+')
    parser.add_argument('-d','--duration', type=TimeDeltaType(), help='Amonut of time to run the motor for', nargs='?')
    args = parser.parse_args()

    motors = [hw.motors[hw.jointNames.index(j)] for j in args.joints]
    if args.duration == None:
        print "Running %s at %.3f"%(args.joints, args.strength)
        set_motors(motors, args.strength)
    else:
        print "Running %s at %.3f for %.3fs"%(args.joints, args.strength, args.duration.total_seconds())
        set_motors(motors, args.strength)
        time.sleep(args.duration.total_seconds())
        set_motors(motors, 0)
        print "Stopped %s"%(args.joints)
