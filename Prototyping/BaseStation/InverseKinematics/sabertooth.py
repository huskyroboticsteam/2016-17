import serial

class Sabertooth:
	def __init__(self, serialPort, address, channel):
		"""
		serialPort is a serial object that the sabertooth is connected to. 
			Baud rate and output file are specified here
		Address as the device address the sabertooth controller lives on. This
			can be 128, 129 or 130. Each address can have two motors attached to it.
		Channel is the starting channel on the controller that the specific motor
			is connected to. Each controller has two starting channels, 0 and 4.

		Passing in values that don't meet this specification may or may not work. 
		"""
		# Adresses should be 128, 129 or 130 for each pair of motors
		self.ser = serialPort 
		self.address = address
		# Should be 0 or 4
		self.channel_start = channel 

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
