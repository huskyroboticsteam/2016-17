import Adafruit_BBIO.UART as uart
import serial
from time import sleep
from math import *
from sabertooth import *

uart.setup("UART1")
"""
ser = serial.Serial(port = "/dev/ttyO1", baudrate=38400)
ser.close()
ser.open()
power = 0
while ser.isOpen():
	power = power + 1
	if power > 127:
		power = 0
	data = bytearray([128, 0, power, (128 + 0 + power) & 127 ])
	ser.write(data)
	print data
	sleep(.05)
"""

time = 0

wrist_angle = Sabertooth(1)
elbow_angle = Sabertooth(2)
# Motors 4 and 5 must run at Baud 9600
test = Sabertooth(5, 9600)

try:
	while True:
		#for i in xrange(4):
		#	motors[i].write(sin(time + (pi/2 * i)))
		#time += .05
		#sleep(.02)
		test.write(-.5)
except KeyboardInterrupt:
	#for i in xrange(4):
	#	motors[i].close()
		test.close()

