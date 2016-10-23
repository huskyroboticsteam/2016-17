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

# Initialize text color.
color = (255,255,0)

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

        # Check keyboard for key-presses
        if event.type == pygame.KEYDOWN:
            inputKey = event.key # The key that got pressed...
            if inputKey == pygame.K_z: # If it's z, do this
                color = (255,0,0)
            elif inputKey == pygame.K_x: #If it's x, do this
                color = (0,255,0)
            elif inputKey == pygame.K_c:
                color = (0,0,255)

    # Create a text object. This uses the font object to create an object that has actual text and a color. Arguments: (text, antialiasing level, color(R,G,B))
    # Its color can change on each frame so we need to re-create it when color is updated. To make it even better, we can update it only when color changes.
    text1 = font1.render("Hello World", 1, color)

    # Render the text to the screen at position (20,20).
    screen.blit(text1, (20, 20))

    # Update the screen.
    pygame.display.flip()

    # Tell Pygame we have completed the loop.
    pygame.event.pump()