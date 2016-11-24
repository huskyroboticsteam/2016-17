import io
import sys, pygame
from Tkinter import *

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

#https://www.pygame.org/docs/ref/joystick.html

clock = pygame.time.Clock()
fps = 60

size = width,height = 1200,720
black = 0,0,0

screen = pygame.display.set_mode(size)
background = pygame.image.load("MarsDesertResearchStation.png")
cursor = pygame.image.load("cursor.png")
ledOff = pygame.image.load("redBall.png")
ledOn = pygame.image.load("greenBall.png")
ledBackground = pygame.image.load("greyBall.png")
myfont = pygame.font.SysFont("monospace", 20, bold = True)
degree = 45

x, y = 0, 0

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()
    screen.fill(black)
    screen.blit(background,(0, 0))
    screen.blit(ledBackground, (1100, 10))

    if pygame.joystick.get_count() == 0:
        # render text
        label1 = myfont.render("No Joysticks", 1, black)
        label2 = myfont.render("Connected", 1, black)
        screen.blit(label1, (1050, 70))
        screen.blit(label2, (1065, 85))

        # flash led
        screen.blit(ledOff, (1100, 10))

    else:
        # render text
        if pygame.joystick.get_count() == 1 :
            label1 = myfont.render(str(pygame.joystick.get_count()) + " Joystick", 1, black)
        else:
            label1 = myfont.render(str(pygame.joystick.get_count()) + " Joysticks", 1, black)

        label2 = myfont.render("Connected", 1, black)
        screen.blit(label1, (1060, 70))
        screen.blit(label2, (1065, 85))

        # flash led
        screen.blit(ledOn, (1100, 10))
        mainJoystick = pygame.joystick.Joystick(0)
        mainJoystick.init()

        # update cursor
        axisx = round(mainJoystick.get_axis(0), 0)
        axisy = round(mainJoystick.get_axis(1), 0)

        cursor = pygame.image.load("cursor.png")

        #START OF ROTATION CODE
        #----------------------
        #draw surf to screen and catch the rect that blit returns
        blittedRect = cursor.get_rect()
        blittedRect = blittedRect.move(x, y)

        ##ROTATED
        #get center of surf for later
        oldCenter = blittedRect.center

        #rotate surf by DEGREE amount degrees
        rotatedSurf =  pygame.transform.rotate(cursor, degree)

        #get the rect of the rotated surf and set it's center to the oldCenter
        rotRect = rotatedSurf.get_rect()
        rotRect.center = oldCenter

        #draw rotatedSurf with the corrected rect so it gets put in the proper spot
        screen.blit(rotatedSurf, rotRect)

        #change the degree of rotation
        degree += 5
        degree = degree % 360

        x += axisx
        y += axisy
        print(x, y)

    pygame.display.flip()
    pygame.event.pump()