import pygame

class CameraMovement:

    camOneUD = 0
    camOneLR = 0
    camTwoUD = 0
    camTwoLR = 0

    def keyPressed(self, inputKey):

        if (inputKey == pygame.K_UP):
            self.camOneUD = 1
        elif (inputKey == pygame.K_DOWN):
            self.camOneUD = -1
        elif (inputKey == pygame.K_RIGHT):
            self.camOneLR = 1
        elif (inputKey == pygame.K_LEFT):
            self.camOneLR = -1

        if (inputKey == pygame.K_W):
            self.camTwoUD = 1
        elif (inputKey == pygame.K_S):
            self.camTwoUD = -1
        elif (inputKey == pygame.K_D):
            self.camTwoLR = 1
        elif (inputKey == pygame.K_A):
            self.camTwoLR = -1

    def resetCameras(self):
        self.camOneUD = 0
        self.camOneLR = 0
        self.camTwoUD = 0
        self.camTwoLR = 0

    def addInput(self, messageUDP):
        messageUDP = messageUDP.join(self.camOneUD, self.camOneLR, self.camTwoUD, self.camTwoLR);
        self.resetCameras()
        return messageUDP






