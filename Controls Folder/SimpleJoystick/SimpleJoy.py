# A simple one joystick capture for sending thrust and turn to arduino.
import pygame
from time import sleep
pygame.init()
joystick1 = pygame.joystick.Joystick(0)
joystick1.init()

print joystick1.get_id()

print joystick1.get_numaxes()

print joystick1.get_numbuttons()

exitFlag = False
while not exitFlag and joystick1.get_init():
    sleep(.5)
    print "AXIS:"
    #for x in range(joysticks[0].get_numaxes()):
    print joystick1.get_axis(0)
        #print str(x) + ': ' + str(joysticks[0].get_axis(0))
    #print "BUTTONS:"

    #for x in range(joysticks[0].get_numbuttons()):
     #   print str(x) + ': ' + str(joysticks[0].get_button(x))
