import pygame
import Map
import sys


class PygameWrapper:
    def __init__(self, width, height):

        self.m = Map.Map()
        pygame.font.init()

        # Display dimensions to 1600 x 1100
        self.screen = pygame.display.set_mode((1600, 1100))

        # Objects that will control fps
        self.clock = pygame.time.Clock()
        self.fps = 120


    def main_loop(self):

        # Loop fps times per second
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            # Close if the exit button is pressed
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                inputKey = event.key  # The key that got pressed...

                # Zoom in if z is pressed
                if inputKey == pygame.K_z:  # If it's z, do this
                    self.m.zoom_in()

                # Zoom out if x is pressed
                elif inputKey == pygame.K_x:  # If it's x, do this
                    self.m.zoom_out()

                elif inputKey == pygame.K_0:
                    self.m.get_mouse_lat_lng(pygame.mouse.get_pos())

                elif inputKey == pygame.K_END:
                    self.screen.fill((0, 0, 0))
                    pygame.display.flip()
                    self.m.open_map()

            # Move the tiles if you're moving the mouse with left button down
            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    # clicked and moving
                    rel = event.rel
                    # Pass the dx and dy to the move_map function
                    self.m.move_map(rel[0], rel[1])

        # Fill with black, display, and update
        self.screen.fill((0, 0, 0))
        self.m.display(self.screen)
        pygame.display.flip()
        pygame.event.pump()
