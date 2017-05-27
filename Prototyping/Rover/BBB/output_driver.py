import serial
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
import atexit

class Output:
    """
    A generic one axis output device. Accepts values -1 to 1.
    Make sure to close it when done.
    
    Implementing classes should override write and close, as well as
    safely stop operation of an attached device when close is called.
    (This may be done by calling self.write(0) in close)
    
    Any subclass of output may also be used in a try/with block
    """
    def write(self, value):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

	# Resource management
	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.close()

class Sabertooth(Output):
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

	def close(self):
		self.write(0)
		self.ser.close()

	def write(self, value):
		"""
		Writes a value from -1 to 1 for reverse and forward
        This uses the packetized serial mode of the sabertooth
        Designed for 2X5, but also is known to work with 2X25
        
        Algorithm adapted from the sabertooth documentation
		"""

		channel = self.channel_start + 1 if (value < 0) else self.channel_start
		power = int(abs(value) * 127) # 127 is the max value to send
		checksum = (self.address + channel + power) & 127
		data = bytearray([self.address, channel, power, checksum])
		self.ser.write(data)

class TalonOutput(Output):
    def __init__(self, outputPin, powerPin=None, groundPin=None):
        """
        Pins are strings like 'P9_24'. If power or ground is None, no
        pins will be driven high or low.
        """
        self.outputPin = outputPin
        self.powerPin = powerPin
        self.groundPin = groundPin  
        
        PWM.start(outputPin, 37.5)
        PWM.set_frequency(outputPin, 1 / .004)
        
        # This may not be nececary, but I've included it anyways
        if powerPin is not None:
            GPIO.setup(powerPin, GPIO.IN)
            GPIO.output(powerPin, GPIO.HIGH)
            
        if groundPin is not None:
            GPIO.setup(groundPin, GPIO.IN)
            GPIO.output(groundPin, GPIO.LOW)
            
        self.write(0)
        
    def write(self, value):
        output = (value + 1) / 2.0
        PWM.set_duty_cycle(self.outputPin, 25 + output * 25)
        
    def close(self):
        self.write(0)
        PWM.stop(self.outputPin)
        
        
def exit_handler():
    PWM.cleanup()
    GPIO.cleanup()
    
atexit.register(exit_handler)
