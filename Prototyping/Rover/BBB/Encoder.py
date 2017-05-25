import Adafruit_BBIO.GPIO as GPIO

class Encoder:
    """
    This runs at a lower than posssible frequency because I don't feel like implementing a more accurate
    version, and I'm worried the interrupts are too costly
    """
    def __init__(self, pinA, pinB):
        self.count = 0
        
        GPIO.setup(pinA, GPIO.IN)
        GPIO.setup(pinB, GPIO.IN)

        GPIO.add_event_detect(pinA, GPIO.RISING, callback=self.updatePosition) # bouncetime = 300
        # GPIO.add_event_detect(pinB, GPIO.BOTH, callback=self.updatePosition)
    
    def updatePosition(self):
        if GPIO.input(pinB):
           self.count += 1
        else:
            self.count -= 1
            
