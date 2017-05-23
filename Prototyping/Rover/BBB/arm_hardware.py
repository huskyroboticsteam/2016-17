import Adafruit_BBIO.UART as uart
import serial
import time

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

"""
Pin 1- Ground
Pin 6- System 5V Powers the beagle bone- needs to be set
Pin 8- Output 5V to power encoders- needs to be set
Motor controller pins don't change
Pin 37/39 feedback for linear actators. Connected to pots. Analog
Pin 3, 5, 7, 9, 11, 13, 15, 17. Paired A then B for encoder feedback. First set is BA
Base rotation talon connected to 18, 20 and 22- PWM
- 20 is signal
- Power is the others
"""

jointNames = ["base_rotation", "shoulder", "elbow", "wrist_lift", "wrist_rotation", "hand_grip"]

motors = {}
motors[0] = Sabertooth(ser2, 128, 0)
motors[1] = Sabertooth(ser1, 130, 0)
motors[2] = Sabertooth(ser2, 128, 4)
motors[3] = Sabertooth(ser2, 129, 4)
motors[4] = Sabertooth(ser1, 130, 4)
motors[5] = Sabertooth(ser2, 129, 0)

feedback = {}