import re

# Section below is testing only
# --------------------------------------------------------------------------------------
def main():
	bleh = coords("40.1231,-122*3147*471.23")
	print bleh.latitude
	print bleh.longitude

# Splits input.  Separate DMS using whatever you want as long as it's not a decimal point,
# negative sign or comma.  commas separate lat, long
# --------------------------------------------------------------------------------------
class coords:
	def __init__(self, current_string):
		s = current_string.split(',') 
		tempLat = self.splitInput(s[0])
		tempLong = self.splitInput(s[1])
		self.latitude = self.format(tempLat)
		self.longitude = self.format(tempLong)

	# separates out all non-numeric values 
	def splitInput(self, s):
		temp = filter(None, re.split(r'[^-\d.]+', s))
		return self.castToFloat(temp)

	def castToFloat(self, arr):
		return [float(i) for i in arr]

	def convertToDec(self, arr):
		dec = 0;
		for i in range(len(arr)):
			dec += arr[i] / (60**i)
		return dec

	def format(self, arr):
		if len(arr) == 1:
			return float(arr[0]) # returns float if it is in standard format
		else:
			return self.convertToDec(arr) # converts DMS format to decimals

# --------------------------------------------------------------------------------------

if __name__ == "__main__":
	main()
