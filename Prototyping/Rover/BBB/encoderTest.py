import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_7", GPIO.IN)
GPIO.setup("P8_8", GPIO.IN)
count = 0



def encoder(channel):
    global count
    count += 1

GPIO.add_event_detect("P8_7", GPIO.BOTH, callback=encoder)

while True:
    print str(count)