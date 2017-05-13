import os
import datetime
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
in_pin = 16
GPIO.setup(in_pin, GPIO.IN)
while True:
    try:
        GPIO.wait_for_edge(in_pin, GPIO.FALLING)
        name = (''.join(str(datetime.datetime.now()).split(".")).replace(" ","") + '.jpg')
        command = "fswebcam -r 1600x1200 " + name
        print(command)
        os.system("ping 8.8.8.8")
        #os.system(command)
    except KeyboardInterrupt:
        GPIO.cleanup()
GPIO.cleanup()
