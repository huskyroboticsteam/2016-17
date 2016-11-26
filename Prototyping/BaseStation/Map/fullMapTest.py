import Map
import pygame
import sys

m = Map.Map()
new = raw_input("Generate New Map (Y/N): ")

if new == "Y" or new == "y":
    m.generate_maps()

m.build_tiles()
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
            elif inputKey == pygame.K_0:
                m.printStuff()
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                # clicked and moving
                rel = event.rel
                # Pass the dx and dy to the move_map function
                m.move_map(rel[0], rel[1])

    screen.fill((0, 0, 0))
    m.display(screen)
    pygame.display.flip()
    pygame.event.pump()