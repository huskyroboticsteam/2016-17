import Map
import pygame
import sys

# Make a new map object
m = Map.Map()

# Display dimensions to 1600 x 1100
screen = pygame.display.set_mode((1600, 1100))

# Objects that will control fps
clock = pygame.time.Clock()
fps = 60

while True:
    # Loop fps times per second
    clock.tick(fps)

    for event in pygame.event.get():
        # Close if the exit button is pressed
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            inputKey = event.key  # The key that got pressed...

            # Zoom in if z is pressed
            if inputKey == pygame.K_z:  # If it's z, do this
                m.zoom_in()

            # Zoom out if x is pressed
            elif inputKey == pygame.K_x:  # If it's x, do this
                m.zoom_out()

        # Move the tiles if you're moving the mouse with left button down
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                # clicked and moving
                rel = event.rel
                # Pass the dx and dy to the move_map function
                m.move_map(rel[0], rel[1])

    # Fill with black, display, and update
    screen.fill((0, 0, 0))
    m.display(screen)
    pygame.display.flip()
    pygame.event.pump()