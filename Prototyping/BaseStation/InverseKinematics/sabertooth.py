import serial

class Sabertooth:
	def __init__(self, motor_num, baud_rate=38400):
		"""
		Motor_num should be between 1-6
		"""
		# Adresses should be 128, 129 or 130 for each pair of motors
		self.address = (motor_num / 2) + 128
		# Should be 0 or 4 depending on odd or even
		self.channel_start = (motor_num % 2) * 4 
		self.ser =  serial.Serial(port = "/dev/ttyO1", baudrate=baud_rate)

	# Resource management
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

	def close(self):
		self.write(0)
		self.ser.close()

	def write(self, value):
		"""
		Writes a value from -1 to 1 for reverse and forward
		"""

		channel = self.channel_start + 1 if (value < 0) else self.channel_start
		power = int(abs(value) * 127) # 127 is the max value to send
		checksum = (self.address + channel + power) & 127
		data = bytearray([self.address, channel, power, checksum])
		self.ser.write(data)
