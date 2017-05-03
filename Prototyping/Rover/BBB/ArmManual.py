import armcontrol as ac

# Controls the arm with manual (joystick) controls

comms = Arm_comms("192.168.1.8", 53204, "control_format")

while True:
    comms.receiveData()
    
    # Use this to move the arm
    # comms.receivedDrive