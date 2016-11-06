__author__ = 'Trevor'

import pygame
import sys

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((700,300))

font1 = pygame.font.SysFont("", 150)
text1 = font1.render("Hello World", 1, (213, 202, 148))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(text1, (20, 20))
    pygame.display.flip()
    pygame.event.pump()