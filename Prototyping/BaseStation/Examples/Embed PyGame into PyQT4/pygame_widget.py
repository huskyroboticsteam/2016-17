import pygame

import ui

pygame.font.init()

class PyGameWidget():
    def __init__(self, width, height):

        self.display = pygame.display
        self.display.init()

        self.display.set_mode((width, height))

        # Fill surface with black
        self.display.get_surface().fill((0, 0, 0, 0))

        # Create "Hello World" using the default font
        self.font1 = pygame.font.SysFont("", 150)

        self.color = (201,201,201)

        self.data = "DATA"


    def main_loop(self):

        self.display.flip()

        self.data = "Joy input"
        for event in pygame.event.get():

            # Check keyboard for key-presses
            if event.type == pygame.KEYDOWN:
                inputKey = event.key  # The key that got pressed...
                if inputKey == pygame.K_z:  # If it's z, do this
                    self.color = (255, 0, 0)
                elif inputKey == pygame.K_x:  # If it's x, do this
                    self.color = (0, 255, 0)
                elif inputKey == pygame.K_c:
                    self.color = (0, 0, 255)

        text1 = self.font1.render("Hello World", 1, self.color)

        # Render the text to the screen at position (20,20).
        self.display.get_surface().blit(text1, (20, 20))

        print(pygame.mouse.get_pos())

        # Tell Pygame we have completed the loop.
        pygame.event.pump()

if __name__ =='__main__':
    ui.createUI(700, 300)
