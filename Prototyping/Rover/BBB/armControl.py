#!/usr/bin/env python
import Adafruit_BBIO.UART as uart
import serial
from math import *
from sabertooth import *
import atexit

uart.setup("UART1")
uart.setup("UART2")
ser1 = serial.Serial(port="/dev/ttyO1", baudrate=9600) # Pin 24
ser2 = serial.Serial(port="/dev/ttyO2", baudrate=38400) # Pin 21
ser1.close()
ser2.close()
ser1.open()
ser2.open()

def exit_handler():
    ser1.close()
    ser2.close()
    
atexit.register(exit_handler)


motors = {}
motorNames = ["base_rotation", "shoulder", "elbow", "wrist_lift", "wrist_rotation", "hand_grip"]
motors[0] = Sabertooth(ser2, 128, 0)
motors[1] = Sabertooth(ser1, 130, 0)
motors[2] = Sabertooth(ser2, 128, 4)
motors[3] = Sabertooth(ser2, 129, 4)
motors[4] = Sabertooth(ser1, 130, 4)
motors[5] = Sabertooth(ser2, 129, 0)

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
    parser.add_argument('joints', choices=motorNames, help='The joint to control.', nargs='+')
    parser.add_argument('-d','--duration', type=TimeDeltaType(), help='Amonut of time to run the motor for', nargs='?')
    args = parser.parse_args()

    motors = [motors[motorNames.index(j)] for j in args.joints]
    if args.duration == None:
        print "Running %s at %.3f"%(args.joints, args.strength)
        set_motors(motors, args.strength)
    else:
        print "Running %s at %.3f for %.3fs"%(args.joints, args.strength, args.duration.total_seconds())
        set_motors(motors, args.strength)
        time.sleep(args.duration.total_seconds())
        set_motors(motors, 0)
        print "Stopped %s"%(args.joints)
