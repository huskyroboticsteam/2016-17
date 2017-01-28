import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
pwm.set_pwm_freq(60)
for i in range(0, 4097, 256):
    print str(i)
    pwm.set_pwm(7, i, 4096 - i)
    pwm.set_pwm(6, 0, 4096)
    pwm.set_pwm(5, 4096, 0)
    time.sleep(1)
