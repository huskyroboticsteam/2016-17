
class obsAvoi :
# A work in progress

    def __init__(self, LP, RP):
        self.POT_LEFT = LP
        self.POT_RIGHT = RP
        self.POT_MIDDLE = (self.POT_LEFT + self.POT_RIGHT) / 2

    # TODO: Use sensor in front of rover to determine if there is a
    #       an obstacle within a certain threshold in front
    def isObsticle (self, distance):
        return false

    # Looks around for obstacles and returns a heading without one
    def getDetourHeading(self):
        possibleHeadings = []
        # Stop the rover
        for i in range(1, 5):
            robot.driveMotor(i, 0)
        # Make the rover look as far left as possible
        while(readPot < POT_LEFT):
            robot.driveMoter(1, 20)
            robot.driveMoter(3, 20)
        robot.driveMoter(1, 0)
        robot.driveMoter(3, 0)
        # Look from left to right gathering obstacles in an arc ahead
        while(readPot > POT_Right):
            robot.driveMoter(1, -20)
            robot.driveMoter(3, -20)
            possibleHeadings.append((getMag(), isObsticle))
            #TODO: Maybe? Add pause to slow read speed
        Robot.driveMoter(1, 0)
        Robot.driveMoter(3, 0)
        searchHeading = false
        # Determine path closest to center with no obstacle
        while (searchHeading):
            middleHeading = int(len(possibleHeadings) / 2)
            tempHeading = possibleHeadings.pop(self, middleHeading)
            # Check for next value to the right of center
            if (not tempHeading[1]):
                return tempHeading[0]
            tempHeading = possibleHeadings.pop(self, middleHeading -1)
            # Check for next vale to the left of center
            if (not tempHeading[1]):
                return tempHeading[0]