#######################################
# Code coded by Mike Doty
#
# If you want trackball checking, you will
# have to code it yourself.  Sorry!
#
# Oh, and it just grabs the first joystick.
#   Yes, that makes me lazy.
#
# Released February 8, 2008.
#######################################
import serial
import pygame
from pygame.locals import *
from struct import *

ser = serial.Serial('/dev/cu.HC-05-DevB')

class App:
    forward = False
    back = False
    left = False
    right = False
    stop = False
    directions = array(forward, back, left, right, stop)

    def __init__(self):
        
        pygame.init()

        pygame.display.set_caption("Joystick Analyzer")

        # Set up the joystick
        pygame.joystick.init()

        self.my_joystick = None
        self.joystick_names = []

        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

        print self.joystick_names

        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()

        max_joy = max(self.my_joystick.get_numaxes(),
                      self.my_joystick.get_numbuttons(),
                      self.my_joystick.get_numhats())

        self.screen = pygame.display.set_mode((max_joy * 30 + 10, 170))

        self.font = pygame.font.SysFont("Courier", 20)

    # A couple of joystick functions...
    def check_axis(self, p_axis):
        if (self.my_joystick):
            if (p_axis < self.my_joystick.get_numaxes()):
                return self.my_joystick.get_axis(p_axis)

        return 0

    def check_button(self, p_button):
        if (self.my_joystick):
            if (p_button < self.my_joystick.get_numbuttons()):
                return self.my_joystick.get_button(p_button)

        return False

    def check_hat(self, p_hat):
        if (self.my_joystick):
            if (p_hat < self.my_joystick.get_numhats()):
                return self.my_joystick.get_hat(p_hat)

        return (0, 0)

    def send_command(self):
        throttle = self.check_axis(1)
        turn = self.check_axis(2)
        if(throttle < -0.5 and not forward):
            reset()
            forward = True
            ser.write('f')
        elif(throttle > 0.5 and not back):
            reset()
            back = True
            ser.write('r')
        elif(not stop):
            reset()
            stop = True
            ser.write('s')

    def reset(direction):
        for each in directions:
            each = False


    def main(self):
        self.UDP_init()
        while (True):
            self.g_keys = pygame.event.get()

            self.screen.fill(0)

            for event in self.g_keys:
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.quit()
                    return

                elif (event.type == QUIT):
                    self.quit()
                    return

            self.send_command()

    def quit(self):
        pygame.display.quit()


app = App()
app.main()