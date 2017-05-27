import Adafruit_BBIO.UART as uart
import serial
import time
import atexit
from output_driver import *

uart.setup("UART1")
uart.setup("UART2")
ser2 = serial.Serial(port="/dev/ttyO1", baudrate=38400) # Pin 24
ser1 = serial.Serial(port="/dev/ttyO2", baudrate=9600) # Pin 21
ser1.close()
ser2.close()
ser1.open()
ser2.open()

# Helps automatic baud rate decection
# ser1.write(bytearray([170]))

"""
Pin 1- Ground
Pin 6- System 5V Powers the beagle bone- needs to be set
Pin 8- Output 5V to power encoders- needs to be set
Motor controller pins don't change
Pin 37/39 feedback for linear actators. Connected to pots. Analog
Pin 3, 5, 7, 9, 11, 13, 15, 17. Paired A then B for encoder feedback. First set is BA
Base rotation talon connected to 14 - PWM
"""

jointNames = ["base_rotation", "shoulder", "elbow", "wrist_lift", "wrist_rotation", "hand_grip"]

# Out means towards full extension

motors = {}
motors[0] = TalonOutput("P9_14")
motors[1] = Sabertooth(ser1, 130, 0) # Positive is out
motors[2] = Sabertooth(ser2, 128, 0) # Negitive is out
motors[3] = Sabertooth(ser2, 128, 4) # Positive is out
motors[4] = Sabertooth(ser1, 130, 4) # Positive is clockwise
motors[5] = Sabertooth(ser2, 129, 4) # Positive is out

feedback = {}
#feedback[0] = Encoder()


def exit_handler():
    ser1.close()
    ser2.close()
    
    for i in xrange(len(motors)):
        try:
            motors[i].close()
        except:
            pass
    
atexit.register(exit_handler)