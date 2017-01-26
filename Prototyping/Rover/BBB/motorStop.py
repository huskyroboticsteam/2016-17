import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685(address=0x60, busnum=1)
pwm.set_pwm_freq(60)
pwm.set_pwm(8,2048,2048)
pwm.set_pwm(13,2048,2048)
pwm.set_pwm(2,2048,2048)
pwm.set_pwm(7,2048,2048)