__author__ = 'Trevor'

def pixelToCoord(self,x,y):
    coord = (self.MapArray[self.currentMap].startingLocation[0] - self.MapArray[self.currentMap].borderDistance[0] / 640 * (y - 320), #latitude
             self.MapArray[self.currentMap].startingLocation[1] + self.MapArray[self.currentMap].borderDistance[1] / 640 * (x - 320)) #longitude
    return coord

def coordToPixel1(latitude,longitude,currentMap):
    #print currentMap.ULcoord
    #print currentMap.URcoord
    #print currentMap.LLcoord
    #print currentMap.LRcoord
    latSpan = abs(currentMap.ULcoord[0] - currentMap.LLcoord[0]) # Total latitudinal map span
    longSpan = abs(currentMap.URcoord[1] - currentMap.ULcoord[1]) # Total longitudinal map span
    pixSpanx = currentMap.dimensions[1]*640
    pixSpany = currentMap.dimensions[0]*640
    latTransform = abs(latitude - currentMap.ULcoord[0])
    longTransform = abs(longitude - currentMap.ULcoord[1])
    #print latSpan
    #print longSpan
    #print latTransform
    #print longTransform
    positionX = longTransform*(pixSpanx/longSpan)
    positionY = latTransform*(pixSpany/latSpan)
    #print (positionX,positionY)
    return (positionX,positionY)