import Adafruit_BBIO.PWM as PWM
try:
    PWM.start("P9_14", 150/17.6, 60)
    PWM.set_duty_cycle("P9_14", 150/17.6)
except:
    pass
try:
    PWM.start("P9_16", 150/17.6, 60)
    PWM.set_duty_cycle("P9_16", 150/17.6)
except:
    pass
try:
    PWM.start("P8_22", 150/17.6, 60)
    PWM.set_duty_cycle("P8_13", 150/17.6)
except:
    pass
try:
    PWM.start("P8_21", 150/17.6, 60)
    PWM.set_duty_cycle("P8_19", 150/17.6)
except:
    pass
