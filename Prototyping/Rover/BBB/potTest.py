import Adafruit_BBIO.ADC as ADC

ADC.setup()
while True:
    potVal = ADC.read("AIN0")
    print(potVal)