__author__ = 'Trevor'

import colors
from MapTile import *
from VisualObjects import *


class DisplayScreen:
    def __init__(self, pygame, screenWidth, screenHeight):
        self.pygame = pygame
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.fullscreenToggle = False
        self.screen = pygame.display.set_mode((screenWidth,screenHeight))

        # Set the window title/caption TODO: add image
        pygame.display.set_caption("Husky Robotics Hot GUI")

        # Set fps
        self.clock = pygame.time.Clock()
        self.fps = 60

class DisplayBoxes(DisplayScreen):
    def __init__(self, pygame, screenWidth, screenHeight, numberOfJoysticks):
        DisplayScreen.__init__(self, pygame, screenWidth, screenHeight)
        margin = 20
        self.numberOfJoysticks = numberOfJoysticks
        self.rect = [(margin,margin,(self.screenWidth-margin*3)/2,(self.screenHeight-margin*3)/2), ((self.screenWidth-margin*3)/2 + 40,20,(self.screenWidth-margin*3)/2,(self.screenHeight-margin*3)/2), (20,(self.screenHeight-margin*3)/2+40,(self.screenWidth-margin*3)/2,(self.screenHeight-margin*3)/2), ((self.screenWidth-margin*3)/2 + 40,(self.screenHeight-margin*3)/2 + 40,(self.screenWidth-margin*3)/2,(self.screenHeight-margin*3)/2)]

    def display(self, numberOfConnectedJoysticks):
        self.clock.tick(self.fps)
        print numberOfConnectedJoysticks
        for i in range(0,self.numberOfJoysticks):
            if i < numberOfConnectedJoysticks:
                color = (255,0,0)
            else:
                color = (80,0,0)
            self.pygame.draw.rect(self.screen,color,self.rect[i])
        self.pygame.display.flip()

class DisplayInterface(DisplayScreen):
    def __init__(self, pygame, screenWidth, screenHeight):
        DisplayScreen.__init__(self, pygame, screenWidth, screenHeight)

        # Define maps.
        startingCoord = (38.300585, -111.404652) # Point more than 1km away from the URC site: (38.420358,-110.809686) For UW: (47.656874,-122.312135) For Hotel: (38.300585, -111.404652)
        ArraySize = [(4,4),(4,4),(4,4),(8,8),(4,4)] # Size of 640x640 tile array for each zoom level separated by commas.
        locationName = "Hotel" #UW, Mars, and Hotel are the options
        self.zoomLevels = [17,18,19,20,21]  # zoom levels to make displayable on map. Google does not go higher than 21 in Utah.
        self.MapArray = []

        self.MainAxis = axis(0,0)
        self.currentMap = 2  # Start at this map zoom level (entry in zoomLevel array: 2 corresponds to 19)

        self.PixelLocation = False

        for i in range(len(self.zoomLevels)):
            mapName = locationName + "map" + str(self.zoomLevels[i])
            self.MapArray.append(Map(self.pygame, mapName, ArraySize[i], startingCoord, self.zoomLevels[i]))

        self.MapTiles = self.loadImages(self.MapArray[self.currentMap])

        # Load other generic images
        self.Ball = pygame.image.load("ballcrosshair.png") # 50x50 pixel image
        self.RoverBall = pygame.image.load("RoverIcon.png")
        self.ScaleIndicatorImage = pygame.image.load("ScaleIndicator160.png")
        self.RoverFrontImage = pygame.image.load("RoverFront175.png")
        self.RoverBackImage = pygame.image.load("RoverBack175.png")

        # Create other objects
        self.SidebarRect = Sidebar(self.pygame,self.screenHeight)
        self.MarkerTextArea = TextArea((25, 400, 150, 100))
        self.CameraSelectionArea = CameraArea()
        self.createButtons()
        self.InputTextbox = Textbox()
        self.RoverPositionMarker = RoverPosition(self.RoverBall)
        self.RoverGraphic = RoverGraphic(self.RoverFrontImage,self.RoverBackImage)
        self.markerList = []

        self.EmergencyButtonsEnabled = False

    def loadImages(self, map): # Take a map object and load its images into memory for display
        mapTiles = [[0 for m in xrange(0, self.MapArray[self.currentMap].dimensions[1])] for n in xrange(0, self.MapArray[self.currentMap].dimensions[0])] # tileArraySize[0] is rows, tileArraySize[1] is columns
        numSaves = 0
        mapUpperLeftCorner = (0,0)
        for n in range(0,map.dimensions[0]):
            for m in range(0,map.dimensions[1]):
                currentCoord = (map.startingLocation[0] - n*map.borderDistance[0], map.startingLocation[1] + m*map.borderDistance[1]) # Subtract from latitude to go south/down (northern hemisphere), add to longitude to go east/right
                mapTiles[n][m] = MapTile(map.name,currentCoord, map.zoom, (640,640), (mapUpperLeftCorner[0] + 640*m, mapUpperLeftCorner[1] + 640*n),self.pygame)
                if mapTiles[n][m].saved:
                    numSaves += 1

        if numSaves > 0:
            print str(numSaves) + " image tiles cached from the Internet."

        # Change the scale based on current map
        self.ScaleIndicatorLine = ScaleIndicator(self.pygame, self.MapArray[self.currentMap].borderDistanceKM/4) # ScaleIndicator image is 160 pixels in length, so take the 640-pixel distance and divide it by 4.
        return mapTiles

    def createButtons(self): # Button(pygame, Xoffset, Yoffset, alignment, widthRatio, heightRatio, screenWidth, screenHeight, staticText, toggleTextFalse, toggleTextTrue, startingStatus = False):
        Font = self.pygame.font.SysFont('Arial', 90*self.screenWidth/3200) # Define font to send to each button - font size adapts based on screen width
        eStopButton = Button(self.pygame,self.screenWidth*3.0/15,self.screenHeight*1.0/15,'Right-aligned',2.0/15,2.0/12,self.screenWidth,self.screenHeight,"ALL","STOP","STOPPED",Font)
        potStopButton = Button(self.pygame,self.screenWidth*5.2/15,self.screenHeight*1.0/15,'Right-aligned',2.0/15,2.0/12,self.screenWidth,self.screenHeight,"POT","STOP","STOPPED",Font)
        self.buttons = [eStopButton,potStopButton]

    def createMarker(self, coord):
        self.markerList.append(Marker(coord,self.MapArray[self.currentMap]))

    def deleteMarker(self):
        for i in range(len(self.markerList)):
            if self.markerList[i] != False:
                if self.markerList[i].Selected == True:
                    self.markerList[i] = False

    def display(self):
        self.clock.tick(self.fps)
        self.screen.fill(colors.BLACK) # Start with black background

        # Render all of the map tiles
        for n in range(0,self.MapArray[self.currentMap].dimensions[0]):
            for m in range(0,self.MapArray[self.currentMap].dimensions[1]):
                self.displaymap(self.MapTiles[n][m].image,self.MapTiles[n][m].screenlocation)

        for i in range(len(self.markerList)): # Display all markers
            if self.markerList[i] != False:
                self.markerList[i].display(self.pygame,self.screen,self.Ball,self.MainAxis)

        # Display rover position
        if self.PixelLocation != False:
            self.RoverPositionMarker.display(self.screen, (self.PixelLocation[0] + self.MainAxis.x,self.PixelLocation[1] + self.MainAxis.y))

        # Render sidebar
        self.SidebarRect.display(self.pygame,self.screen)

        # Display emergency buttons if enabled
        if self.EmergencyButtonsEnabled:
            for i in range(len(self.buttons)):
                self.buttons[i].display(self.pygame, self.screen) # Display every button

        # Display the rover graphic
        self.RoverGraphic.display(self.screen)

        # Display the input textbox
        self.InputTextbox.display(self.pygame,self.screen,self.pygame.font.Font(None,18))

        # Display the box list of points
        self.MarkerTextArea.display(self.screen)

        # Display camera indicators
        self.CameraSelectionArea.display(self.screen)

        # Display the scale indicator
        self.ScaleIndicatorLine.display(self.screen,self.ScaleIndicatorImage)

        # Update display for current frame
        self.pygame.display.flip()

    def clickCheck(self,position):
        if self.EmergencyButtonsEnabled:
            for i in range(len(self.buttons)):
                self.buttons[i].clicked(position)

        for i in range(len(self.markerList)):
            if self.markerList[i] != False:
                self.markerList[i].clicked(position)

    def getEntry(self):
        inputTextboxOut = self.InputTextbox.returnString()
        if inputTextboxOut[1] == 1:
            if inputTextboxOut[0].status == False:
                print "invalid entry"
            else:
                self.createMarker(inputTextboxOut[0])
                self.MarkerTextArea.addTextInstance(pygame.font.Font(None,18),str(inputTextboxOut[0].latitude) + " " + str(inputTextboxOut[0].longitude))
        elif inputTextboxOut[1] == 2:
            dimensions = inputTextboxOut[0].split(',')
            if float(dimensions[0]) >= 500 and float(dimensions[0]) <= 4000 and float(dimensions[1]) >= 500 and float(dimensions[1]) <= 4000: # Sanity check: make sure window resize won't be anything crazy
                self.resizeDisplay(int(dimensions[0]),int(dimensions[1]))
            else:
                print "invalid entry"

    def giveReceivedInformation(self,Coordinate,Magnetometer):
        self.PixelLocation = MapPixelCoords.coordToPixel1(float(Coordinate[0]), float(Coordinate[1]), self.MapArray[self.currentMap])
        print Magnetometer
        MagnetometerNumber = float(Magnetometer) - 180
        if MagnetometerNumber < 0:
            MagnetometerNumber = MagnetometerNumber + 360
        print MagnetometerNumber
        MagneticCorrection = -10.81 # -15.93333 in Seattle, -10.81 in Hanksville
        self.RoverPositionMarker.rotateImage(self.pygame,-MagnetometerNumber+MagneticCorrection)

    def givePotentiometer(self,info):
        angle = 76*info/33-874/3
        self.RoverGraphic.rotateImage(angle)

    def displaymap(self,object,location):
        self.screen.blit(object, (self.MainAxis.x + location[0], self.MainAxis.y + location[1]))

    def resizeMap(self,outOrIn = 'In'):
        if outOrIn == 'In':
            possibleZoomLevel = self.currentMap + 1
        elif outOrIn == 'Out':
            possibleZoomLevel = self.currentMap - 1
        else:
            possibleZoomLevel = 20000 # Won't be in self.zoomLevels for sure
        if (possibleZoomLevel + self.zoomLevels[0]) in self.zoomLevels:
            # Find current central coordinate on screen before updating map
            centralX = -self.MainAxis.x + self.screenWidth/2
            centralY = -self.MainAxis.y + self.screenHeight/2
            mapPoint = MapPixelCoords.pixelToCoord(self, centralX, centralY)
            # Update map
            self.currentMap = possibleZoomLevel
            self.MapTiles = self.loadImages(self.MapArray[self.currentMap])
            # Update marker position
            for i in range(len(self.markerList)):
                if self.markerList[i] != False:
                    self.markerList[i].updateZoom(self.MapArray[self.currentMap])
            # Update screen position
            newPixelCoord = MapPixelCoords.coordToPixel1(mapPoint[0], mapPoint[1], self.MapArray[self.currentMap])
            self.MainAxis.x = -(newPixelCoord[0] - self.screenWidth/2)
            self.MainAxis.y = -(newPixelCoord[1] - self.screenHeight/2)

        else:
            print "You are out of the possible zoom levels."

    def moveMap(self,mouseMovement):
        if (self.MainAxis.x + mouseMovement[0] >= self.SidebarRect.Width):
            self.MainAxis.x = self.SidebarRect.Width
        elif (self.MainAxis.x + mouseMovement[0] <= self.screenWidth-self.MapArray[self.currentMap].PixelWidth):
            self.MainAxis.x = self.screenWidth-self.MapArray[self.currentMap].PixelWidth
        else:
            self.MainAxis.x += mouseMovement[0]
        if (self.MainAxis.y + mouseMovement[1] >= 0):
            self.MainAxis.y = 0
        elif (self.MainAxis.y + mouseMovement[1] <= self.screenHeight-self.MapArray[self.currentMap].PixelHeight):
            self.MainAxis.y = self.screenHeight-self.MapArray[self.currentMap].PixelHeight
        else:
            self.MainAxis.y += mouseMovement[1]

    def resizeDisplay(self, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.SidebarRect = Sidebar(self.pygame,self.screenHeight) # Recreate sidebar with new screenHeight
        self.createButtons() #Recreate all buttons w/ new screenWidth, screenHeight
        if self.fullscreenToggle == False:
            self.setScreenSize()

    def toggleFullscreen(self):
        self.fullscreenToggle = not self.fullscreenToggle
        if self.fullscreenToggle == True:
            self.pygame.display.set_mode((0,0),self.pygame.FULLSCREEN)
        else:
            self.setScreenSize()

    def escapeFullscreen(self):
        if self.fullscreenToggle == True:
            self.fullscreenToggle = False
            self.setScreenSize()

    def setScreenSize(self):
        self.pygame.display.set_mode((self.screenWidth,self.screenHeight))

class axis: #TODO: Move to separate file
    def __init__(self,x,y):
        self.x = x
        self.y = y