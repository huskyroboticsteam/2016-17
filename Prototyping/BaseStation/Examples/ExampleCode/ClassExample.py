__author__ = 'Trevor'

# import necessary libraries to create a GUI window. Pygame does the graphics and user input, and sys handles operating system stuff such as closing the window.
import pygame
import sys

# Initialize the pygame library and the font library
pygame.init()
pygame.font.init()

# Create a "screen" object
screen = pygame.display.set_mode((700,300))

# Set fps
clock = pygame.time.Clock()
fps = 60

# Initialize a font object. (To use a non-default font, there is another way to create a font object in Pygame which you can find on the documentation, which you can find by Googling)
font1 = pygame.font.SysFont("", 150)

# Initialize a text object. This uses the font object to create an object that has actual text and a color. Arguments: (text, antialiasing level, color(R,G,B))
text1 = font1.render("Hello World", 1, (213, 202, 148))

# Main program loop.
while True:

    # Run the program at 60 FPS.
    clock.tick(fps)

    # Check the event queue for input.
    for event in pygame.event.get():
        # If the X has been pressed...
        if event.type == pygame.QUIT:
            # Close the GUI.
            sys.exit()

    screen.fill((0,0,255))

    # Render the text to the screen at position (20,20).
    screen.blit(text1, (20, 20))

    # Update the screen.
    pygame.display.flip()

    # Tell Pygame we have completed the loop.
    pygame.event.pump()