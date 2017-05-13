import armControl as ac
from Arm_comms import *
import time

# Controls the arm with manual (joystick) controls

#192.168.0.80
comms = Arm_comms("192.168.7.2", 53204, "<ffffff")

while True:
    comms.receiveData()
    
    # Use this to move the arm
    if comms.receivedDrive == None:
        print "Nothing recieved"
        for i in xrange(6):
            ac.motors[i].write(0)
    else:
        for i in xrange(6):
            ac.motors[i].write(comms.receivedDrive[i])
    
    time.sleep(1 / 60)