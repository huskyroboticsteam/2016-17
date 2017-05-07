import sys
import Adafruit_BBIO.GPIO as GPIO


def testEnc(channel, it=1000):
    GPIO.setup(channel, GPIO.IN, pull_up_down=1)
    for i in range(0, it):
        if GPIO.input(channel):
            sys.stdout.write("HIGH")
        else:
            sys.stdout.write("LOW")
        sys.stdout.write("\n")

testEnc("P9_22", 1000)
