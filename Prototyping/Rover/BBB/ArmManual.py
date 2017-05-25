import arm_hardware as hw
from Arm_comms import *
import time

# Controls the arm with manual (joystick) controls

# comms = Arm_comms("192.168.7.2", 53204, "<ffffff") # For over USB
comms = Arm_comms("192.168.0.90", 53204, "<ffffff") # For over ethernet

while True:
    comms.receiveData()
    
    # Use this to move the arm
    if comms.receivedDrive == None:
        print "Nothing recieved"
        for i in xrange(6):
            hw.motors[i].write(0)
    else:
        for i in xrange(6):
            hw.motors[i].write(comms.receivedDrive[i])
    
    time.sleep(1 / 60)