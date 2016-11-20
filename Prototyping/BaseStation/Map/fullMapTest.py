import Map
import pygame
import sys

m = Map.Map()
new = raw_input("Generate New Map (Y/N): ")

if new == "Y" or new == "y":
    m.generate_maps()

screen = pygame.display.set_mode((2000, 1500))
clock = pygame.time.Clock()
fps = 60

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            inputKey = event.key  # The key that got pressed...

            if inputKey == pygame.K_z:  # If it's z, do this
                m.zoom_in()
            elif inputKey == pygame.K_x:  # If it's x, do this
                m.zoom_out()

    screen.fill((0, 0, 0))
    m.display(screen)

    pygame.display.flip()
    pygame.event.pump()