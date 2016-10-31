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
        font1 = pygame.font.SysFont("", 150)
        self.text1 = font1.render("Hello World", 1, (213, 202, 148))

    def main_loop(self):

        self.display.flip()

        print(pygame.mouse.get_pos())

        # Render the text to the screen at position (20,20).
        self.display.get_surface().blit(self.text1, (20, 20))

        print(pygame.mouse.get_pos())

        # Tell Pygame we have completed the loop.
        pygame.event.pump()


if __name__ =='__main__':
    ui.createUI(700, 300)








