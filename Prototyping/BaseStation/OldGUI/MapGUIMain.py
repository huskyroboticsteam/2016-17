# Python libraries
import sys
import pygame
from pygame.locals import *

# User-created files
from JoystickConnector import *
from Display import *
from sendOverUDP import *
from receiveOverUDP import *

# Initial screen parameters
screenWidth = 1600
screenHeight = 900

roverAngle = 0

# Start pygame and necessary functionality
pygame.init()
pygame.font.init()

# Run the joystick connection interface if needed
JoystickH = JoystickHandler(pygame) # Joystick handler class
ScreenDisplay = DisplayBoxes(pygame, screenWidth,screenHeight,JoystickH.numberOfJoysticks)

while not JoystickH.joysticksEnabled: # Display loop for joystick connection interface (the 4 boxes), if no joysticks connected, the joystick handler will return True for joysticks enabled and this loop will not run.
    JoystickH.connectJoysticks() # See if any joystick buttons pressed
    ScreenDisplay.display(JoystickH.numberOfConnectedJoysticks) # Update the display
    pygame.event.pump()
    pygame.time.wait(50)

# Now done with joystick connection, switch to regular interface
ScreenDisplay = DisplayInterface(pygame, screenWidth,screenHeight)

# Initialize UDP-sending class that sends data to rover
UDPsender = sendOverUDP("192.168.1.51", 8888) # Main board
#UDPsender2 = sendOverUDP("192.168.1.7", 7777) # Arm
#UDPsender3 = sendOverUDP("192.168.1.52") # Nav
#UDPsender4 = sendOverUDP("192.168.1.7", 7777) # Science
#UDPscienceBALLS = sendOverUDP("192.168.1.53", 8888)
#UDParm = sendOverUDP("192.168.1.52", 8888)
UDPreceiver = receiveOverUDP("192.168.1.40", 8888) #Main
#UDPreceiver2 = receiveOverUDP("192.168.1.40", 7777) #Sci/arm
#UDPreceiver3 = receiveOverUDP("192.168.1.40", 8887) #Nav

# Initialize preset variables
textboxEnabled = False
previousMouseStatus = False

#DEBUG:
Magnetometer = 0
info = 143
EyeSauran = 0
OShit = 0
EyeSauranSend = 0
OShitSend = 0
def checkBounds(cameraValue):
    if cameraValue < 0:
        cameraValueOut = 0
    elif cameraValue > 255:
        cameraValueOut = 255
    else:
        cameraValueOut = cameraValue
    return cameraValueOut

if JoystickH.numberOfJoysticks > 0:
    JoystickPluggedIn = True
else:
    JoystickPluggedIn = False

if JoystickPluggedIn:
    UDPreceiver.start()
    MESSAGE = " "
    RECEIVERTHREADLOCK = threading.Lock()

# MAIN LOOP
while JoystickPluggedIn: # Only run main loop if there is a joystick pluuged in. Seems to prevent rover from taking off.
#while True: # For visual testing ONLY

    # Process values for the joysticks
    JoystickH.scanJoysticks()

    # Mouse panning TODO: add mouse class?
    mousestatus = pygame.mouse.get_pressed()
    if mousestatus[0]:
        movement = pygame.mouse.get_rel()
        if previousMouseStatus == False:
            previousMouseStatus = True
        else:
            ScreenDisplay.moveMap(movement)
    if not mousestatus[0]:
        previousMouseStatus = False

    keysDowned = pygame.key.get_pressed()
    # Other important keyboard states
    if keysDowned[pygame.K_LSHIFT] or keysDowned[pygame.K_RSHIFT]:
        ScreenDisplay.EmergencyButtonsEnabled = True
    else:
        ScreenDisplay.EmergencyButtonsEnabled = False

    #Everything to do with event queue - keys down, etc.
    for event in pygame.event.get():

        # Check if program closed
        if event.type == pygame.QUIT:
            UDPreceiver.End = True
            sys.exit()
        # Check mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            print "yes"
            clickPosition = pygame.mouse.get_pos() # Find position of a mouse click
            ScreenDisplay.clickCheck(clickPosition)

        # Check keyboard
        if event.type == pygame.KEYDOWN:
            inputKey = event.key
            if (inputKey == pygame.K_f): # Enter fullscreen
                ScreenDisplay.toggleFullscreen()
            if (inputKey == pygame.K_ESCAPE): # Escape fullscreen, textbox, whatever
                if ScreenDisplay.InputTextbox.status != 0:
                    ScreenDisplay.InputTextbox.disable()
                else:
                    ScreenDisplay.escapeFullscreen()
            if (inputKey == pygame.K_z): # Zoom out
                ScreenDisplay.resizeMap('Out')
            if (inputKey == pygame.K_x): # Zoom in
                ScreenDisplay.resizeMap('In')
            if (inputKey == pygame.K_m): # Enable coordinate entry mode
                ScreenDisplay.InputTextbox.enableCoordinateEntry()
            if (inputKey == pygame.K_r): # Enable window resizing mode
                ScreenDisplay.InputTextbox.enableWindowResizing()
            if (inputKey == pygame.K_h):
                ScreenDisplay.CameraSelectionArea.switch(0)
            if (inputKey == pygame.K_j):
                ScreenDisplay.CameraSelectionArea.switch(1)
            if (inputKey == pygame.K_k):
                ScreenDisplay.CameraSelectionArea.switch(2)
            if (inputKey == pygame.K_l):
                ScreenDisplay.CameraSelectionArea.switch(3)
            if (inputKey == pygame.K_BACKSPACE):
                ScreenDisplay.InputTextbox.currentString = ScreenDisplay.InputTextbox.currentString[0:-1]
            if (inputKey == pygame.K_RETURN):
                ScreenDisplay.getEntry()
            if (inputKey == pygame.K_DELETE) or (inputKey == pygame.K_BACKSPACE):
                ScreenDisplay.deleteMarker()

            # TESTING INPUT
            if (inputKey == pygame.K_y):
                roverAngle += 10
                ScreenDisplay.RoverGraphic.rotateImage(roverAngle)
            if (inputKey == pygame.K_u):
                Magnetometer += 10
                ScreenDisplay.RoverPositionMarker.rotateImage(pygame, Magnetometer)
            if (inputKey == pygame.K_COMMA):
                EyeSauran += 2
                EyeSauranSend = checkBounds(EyeSauran)
            if (inputKey == pygame.K_PERIOD):
                EyeSauran -= 2
                EyeSauranSend = checkBounds(EyeSauran)
            # if (inputKey == pygame.K_LEFTBRACKET):
            #     OShit += 2
            #     OShitSend = checkBounds(OShit)
            # if (inputKey == pygame.K_RIGHTBRACKET):
            #     OShit -= 2
            #     OShitSend = checkBounds(OShit)
            if (inputKey == pygame.K_c):
                JoystickH.AngleEnabled = 0
            if (inputKey == pygame.K_v):
                JoystickH.AngleEnabled = 1
            if (inputKey == pygame.K_b):
                JoystickH.ScienceSendEnabled = 1
            if (inputKey == pygame.K_n):
                JoystickH.ScienceSendEnabled = 0

            #TODO: Input handling class
            if ScreenDisplay.InputTextbox.status == 1:
                if inputKey == 56 and (pygame.key.get_mods() and KMOD_SHIFT): # If asterisk pressed
                    validKeyIn = True
                    inputKey = 42
                elif (inputKey >= 48 and inputKey <= 57) or inputKey == 44 or inputKey == 46: # If key pressed is in the ASCII number range, or is a comma or period
                    validKeyIn = True
                elif inputKey == 44 or inputKey == 46:
                    validKeyIn = True
                elif inputKey == K_MINUS:
                    validKeyIn = True
                else:
                    validKeyIn = False
            elif ScreenDisplay.InputTextbox.status == 2:
                if (inputKey >= 48 and inputKey <= 57):
                    validKeyIn = True
                else:
                    validKeyIn = False
            else:
                validKeyIn = False

            if validKeyIn == True:
                ScreenDisplay.InputTextbox.currentString.append(chr(inputKey))

    # UDP sending stuff
    AllStopStatus = ScreenDisplay.buttons[0].Status
    PotStopStatus = ScreenDisplay.buttons[1].Status

    print JoystickH.arm_speed
    print JoystickH.armMotors

    JoystickH.sendInput(UDPsender, AllStopStatus, PotStopStatus, OShitSend, EyeSauranSend)
    #JoystickH.sendArmInput(UDPsender2)
    #if JoystickH.ScienceSendEnabled == 0:
    #JoystickH.sendScienceInput(UDPsender4)
    print OShitSend
    print EyeSauranSend
    print "Speed: " + str(JoystickH.Speed)
    print "Angle: " + str(JoystickH.Angle)
    print "Augur: " + str(JoystickH.Augar)
    #print "Drill: " + str(JoystickH.Drill)
    print "Servo: " + str(JoystickH.ServoStatus)
    print "LED: " + str(JoystickH.ScienceSendEnabled)
    print JoystickH.armMotors[0]+127
    print JoystickH.armMotors[1]+127
    print JoystickH.ShoulderRot


    #JoystickH.sendArmInput(UDParm)

    # UDP receiving stuff
    # print UDPreceiver.Coord
    # DEBUG
    # print UDPreceiver.addr

    ScreenDisplay.giveReceivedInformation(UDPreceiver.Coord,UDPreceiver.Magnetometer)
    ScreenDisplay.givePotentiometer(info)
    print UDPreceiver.Coord

    # DRAW EVERYTHING TO SCREEN
    ScreenDisplay.display()

    pygame.event.pump()

# ---------------- end -------------------------------