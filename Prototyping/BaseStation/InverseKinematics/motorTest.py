import Adafruit_BBIO.UART as uart
import serial
from time import sleep
from math import *
from sabertooth import *

uart.setup("UART1")
uart.setup("UART2")
ser1 = serial.Serial(port="/dev/ttyO1", baudrate=9600)
ser2 = serial.Serial(port="/dev/ttyO2", baudrate=38400)
ser1.close()
ser2.close()
ser1.open()
ser2.open()

time = 0
mot_1 = Sabertooth(0, ser_port="/dev/ttyO2")
mot_4 = Sabertooth(1, ser_port="/dev/ttyO2")
wrist_angle = Sabertooth(3, ser_port="/dev/ttyO2")
base_rot = Sabertooth(2, ser_port="/dev/ttyO2")

# Motors 4 and 5 must run at Baud 9600
test = Sabertooth(0, 9600)
test_1 = Sabertooth(1, 9600)
#motors = [Sabertooth(i) for i in xrange(6)]

try:
	while True:
		#for i in xrange(4):
		#	motors[i].write(sin(time + (pi/2 * i)))
		#time += .05
		#sleep(.02)
		wrist_angle.write(0.5)
		base_rot.write(0)
		test.write(0.3)
		mot_1.write(0)
		mot_4.write(0)
		test_1.write(0)
except KeyboardInterrupt:
	#for i in xrange(4):
	#	motors[i].close()
	#	test.close()
	wrist_angle.write(0)
	base_rot.write(0)
	test.write(0)
	mot_1.close()
	mot_4.close()
	wrist_angle.close()
	base_rot.close()
	test_1.close()
	test.close()


