__author__ = 'Trevor'

import string

import pygame

import MapPixelCoords
import colors
from GPSCoordinates import *


class Sidebar:
    def __init__(self,pygame,screenHeight):
        self.Width = 200
        self.Rect = pygame.Surface((self.Width,screenHeight), pygame.SRCALPHA, 32)
        self.Color = (0,0,0,175) # Black but transparent
        self.Rect.fill(self.Color)
    def display(self, pygame, screen):
        screen.blit(self.Rect, (0,0))

class Button:
    def __init__(self, pygame, Xoffset, Yoffset, alignment, widthRatio, heightRatio, screenWidth, screenHeight, staticText, toggleTextFalse, toggleTextTrue, Font, startingStatus = False):
        self.Status = startingStatus

        if alignment == 'Left-aligned':
            X = Xoffset
            Y = Yoffset
        elif alignment == 'Right-aligned':
            X = screenWidth - Xoffset
            Y = Yoffset

        self.Width = screenWidth*widthRatio
        self.Height = screenHeight*heightRatio
        self.X = X
        self.Y = Y
        self.Font = Font
        self.Rectangle = pygame.Rect(X,Y,self.Width,self.Height)

        self.StaticText = Font.render(staticText, 1, colors.GOLD)
        self.ToggleTextFalse = Font.render(toggleTextFalse, 1, colors.GOLD)
        self.ToggleTextTrue = Font.render(toggleTextTrue, 1, colors.GOLD)

        self.StaticTextPos = self.findTextCenterPos(staticText,'Top')
        self.ToggleTextFalsePos = self.findTextCenterPos(toggleTextFalse,'Bottom')
        self.ToggleTextTruePos = self.findTextCenterPos(toggleTextTrue,'Bottom')

        self.check()

    def findTextCenterPos(self, text, alignment = 'Center'):
        textSize = self.Font.size(text)
        X = self.X + (self.Width - textSize[0])/2
        Y = self.Y + (self.Height - textSize[1])/2
        if alignment == 'Top':
            Y -= textSize[1]/2
        elif alignment == 'Bottom':
            Y += textSize[1]/2
        return (X,Y)

    def check(self):
        if self.Status == True: # Update the button's color
            self.Color = colors.WARNINGBOXORANGE
            self.ToggleText = self.ToggleTextTrue
            self.ToggleTextPos = self.ToggleTextTruePos
        else:
            self.Color = colors.DARKBOXRED
            self.ToggleText = self.ToggleTextFalse
            self.ToggleTextPos = self.ToggleTextFalsePos

    def toggle(self):
        self.Status = not self.Status
        self.check()

    def display(self, pygame, screen):
        pygame.draw.rect(screen, self.Color, self.Rectangle)
        screen.blit(self.StaticText,self.StaticTextPos)
        screen.blit(self.ToggleText,self.ToggleTextPos)

    def clicked(self, position):
        if self.Rectangle.collidepoint(position):
            self.toggle()

class Textbox:
    def __init__(self):
        self.TextboxStatus = False
        self.currentString = []
        self.color = colors.WHITE
        self.status = 0
        self.X = 25
        self.Y = 275

    def enableCoordinateEntry(self):
        self.color = colors.HIGHLIGHTBOXRED
        self.status = 1

    def enableWindowResizing(self):
        self.color = colors.HIGHLIGHTBOXGREEN
        self.status = 2

    def disable(self):
        self.color = colors.WHITE
        self.currentString = []
        self.status = 0

    def display(self, pygame, screen, Font):
        if self.status != 0:
            textInBox = Font.render(string.join(self.currentString,""), 0, colors.WHITE) # (text, antialias, (r, g, b))
            screen.blit(textInBox,(self.X+4,self.Y))
        pygame.draw.rect(screen, self.color, (self.X, self.Y, 150, 16), 1) # Draw box (x, y, xlength, ylength, ?)

    def returnString(self):
        string = "".join(self.currentString) # Take an array of chars and join them all together into a single string.
        statusOut = self.status
        if len(string) > 30:
            statusOut = 3 # Make the status invalid if the string is too long and clearly invalid
        if statusOut == 1:
            newString = Coordinates(string)
        elif statusOut == 2:
            newString = string
        else:
            newString = "no"
        self.disable()
        return (newString, statusOut)

class TextArea:
    def __init__(self, rectangle):
        self.X = rectangle[0]
        self.Y = rectangle[1]
        self.Rectangle = rectangle
        self.textInstances = []
        self.activeInstance = -1 # Active instance: the ID for text entry at the top of the box currently. Changes as the list is scrolled through.
        self.instanceCount = 0
        self.endInstance = 0
    def addTextInstance(self,font,text):
        self.textInstances.append(TextInstance(font,text,self.X,self.Y))
        self.instanceCount += 1
        if self.instanceCount > 8:
            self.activeInstance += 1
            self.endInstance = 8
        else:
            self.endInstance = self.instanceCount
    def display(self, screen):
        pygame.draw.rect(screen, colors.GOLD, self.Rectangle, 1)
        for i in range(0,self.endInstance):
            self.textInstances[self.activeInstance+i].display(screen,i)

class TextInstance:
    def __init__(self,font,text,X,Y):
        self.textInBox = font.render(text, 1, colors.GOLD)
        self.X = X
        self.Y = Y
    def display(self, screen, entry):
        screen.blit(self.textInBox,(self.X,self.Y+entry*12))

class Marker:
    notSelectedImage = pygame.image.load("ballcrosshair.png") # 50x50 pixel image
    SelectedImage = pygame.image.load("ballcrosshairBlue.png")
    def __init__(self, coord, initZoomMap):
        self.coord = coord # Absolute location in pixels on map
        self.updateZoom(initZoomMap)
        self.currentCoord = coord # Location of marker on the screen
        self.Xactual = 0
        self.Yactual = 0
        self.Selected = False
    def display(self, pygame, screen, image, axes):
        if self.Selected == True:
            currentImage = Marker.SelectedImage
        else:
            currentImage = Marker.notSelectedImage
        imageSizeCorrection = (-currentImage.get_rect().size[0]/2,-currentImage.get_rect().size[1]/2) # Adds correction to image's coordinates to make it appear at the center of the coordinate given.
        axesPos = (axes.x,axes.y)
        self.Xactual = self.X+axesPos[0]+imageSizeCorrection[0]
        self.Yactual = self.Y+axesPos[1]+imageSizeCorrection[1]
        self.currentRectangle = pygame.Rect(self.Xactual,self.Yactual,50,50)
        screen.blit(currentImage, (self.Xactual,self.Yactual)) # Display each marker at center of given pixel coordinate
    def updateZoom(self, ZoomMap):
        PixelCoord = MapPixelCoords.coordToPixel1(float(self.coord.latitude), float(self.coord.longitude), ZoomMap)
        self.X = PixelCoord[0]
        self.Y = PixelCoord[1]
    def clicked(self, position): # If marker clicked on, toggle its selection status. If click happens anywhere else, deselect.
        if self.currentRectangle.collidepoint(position):
            if self.Selected == True:
                self.Selected = False
            else:
                self.Selected = True
        else:
            self.Selected = False

class ScaleIndicator:
    def __init__(self, pygame, distance):
        Font = pygame.font.SysFont('Arial', 20)
        if distance < 1.0:
            distance *= 1000 # Convert km value to meters if the distance is less than 1 km
            unit = 'meters'
        else:
            unit = 'km'
        distance = round(distance,2)
        self.text = Font.render(str(distance)+' '+unit,1,colors.HIGHLIGHTBOXRED)
        self.X = 20
        self.Y = 750
    def display(self, screen, image):
        screen.blit(image, (self.X,self.Y))
        screen.blit(self.text, (self.X+32,self.Y+25))

class RoverGraphic:
    def __init__(self, image1, image2):
        self.X = 12
        self.Y = 50
        self.image1 = image1
        self.image2 = image2
        self.imgCenter = self.image1.get_rect().center # ImgCenter is the same for both images so only save it once
        self.angularImage1 = image1
        self.angularImage2 = image2
        self.angImgCenter = self.angularImage1.get_rect().center # Angularimagecenter is the same for both images so only save it once
        self.angle = 0
    def display(self, screen):
        screen.blit(self.angularImage1, (self.X-(self.angImgCenter[0]-self.imgCenter[0]),self.Y-(self.angImgCenter[1]-self.imgCenter[1])))
        screen.blit(self.angularImage2, (self.X-(self.angImgCenter[0]-self.imgCenter[0]),self.Y-(self.angImgCenter[1]-self.imgCenter[1])))
    def rotateImage(self, angle):
        self.angle = angle
        if angle != 0:
            self.angularImage1 = pygame.transform.rotozoom(self.image1, angle, 1)
            self.angularImage2 = pygame.transform.rotozoom(self.image2, -angle, 1)
        self.angImgCenter = self.angularImage1.get_rect().center

class RoverPosition:
    def __init__(self, image):
        self.image = image
        self.imgCenter = self.image.get_rect().center
        self.angularImage = image
        self.angImgCenter = self.angularImage.get_rect().center
        self.angle = 0
    def display(self, screen, coord):
        imageSizeCorrection = (-self.image.get_rect().size[0]/2,-self.image.get_rect().size[1]/2) # Adds correction to image's coordinates to make it appear at the center of the coordinate given.
        screen.blit(self.angularImage, (coord[0]-(self.angImgCenter[0]-self.imgCenter[0])+imageSizeCorrection[0],coord[1]-(self.angImgCenter[1]-self.imgCenter[1])+imageSizeCorrection[1]))
        #print coord
    def rotateImage(self, pygame, angle):
        self.angle = angle
        if angle != 0:
            self.angularImage = pygame.transform.rotozoom(self.image, angle, 1)
        self.angImgCenter = self.angularImage.get_rect().center

class CameraArea:
    def __init__(self):
        self.X = 25
        self.Y = 650
        self.Cameras = [Camera("Eye of Sauran", self.X, self.Y, 0),Camera("O Shit", self.X, self.Y, 1),Camera("Arm", self.X, self.Y, 2),Camera("Tom", self.X, self.Y, 3)]
    def display(self, screen):
        for i in range(len(self.Cameras)):
            self.Cameras[i].display(screen)
    def switch(self,id):
        self.Cameras[id].switch()

class Camera:
    def __init__(self,name,X,Y,id):
        self.Name = name
        self.Color = colors.HIGHLIGHTBOXGREEN
        self.Status = True
        self.Rectangle = (X+30*id,Y,20,20)
    def display(self, screen):
        pygame.draw.rect(screen, self.Color, self.Rectangle)
    def switch(self):
        self.Status = not self.Status
        if self.Status == True:
            self.Color = colors.HIGHLIGHTBOXGREEN
        else:
            self.Color = colors.HIGHLIGHTBOXRED