import Adafruit_BBIO.GPIO as GPIO
import time


trig_p = "p8_8"
echo_p = "p8_10"
pulse_start = 0
pulse_end = 0

GPIO.setup(trig_p, GPIO.OUT)
GPIO.setup(echo_p, GPIO.IN)

GPIO.output(trig_p, GPIO.HIGH)
time.sleep(0.00005)
GPIO.output(trig_p, GPIO.LOW)
GPIO.cleanup()

#GPIO.setup(echo_p, GPIO.IN)

while GPIO.input(echo_p) == 1:
    pulse_start = time.time()

while GPIO.input(echo_p) == 0:
    pulse_end = time.time()

pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
print "Distance:", distance, "cm"
GPIO.cleanup()
