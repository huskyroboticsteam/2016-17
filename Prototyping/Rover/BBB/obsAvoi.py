import Robot

class obsAvoi :
# Obstacle Avoidance
# A work in progress
# Assumes it will be placed within
# Will work on making it better after Robot.py refactor

    def __init__(self, LP, RP):
        self.POT_LEFT = LP
        self.POT_RIGHT = RP
        self.POT_MIDDLE = (self.POT_LEFT + self.POT_RIGHT) / 2

    # TODO: Use sensor in front of rover to determine if there is a
    #       an obstacle within a certain distance in front
    #       Waiting for code from science subteam
    def isObstacle (self, distance):
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
            robot.driveMoter(4, 20)
        robot.driveMoter(1, 0)
        robot.driveMoter(4, 0)
        # Look from left to right gathering obstacles in an arc ahead
        while(readPot > POT_Right):
            robot.driveMoter(1, -20)
            robot.driveMoter(4, -20)
            possibleHeadings.append((getMag(), isObstacle))
            #TODO: Maybe? Add pause to slow read speed
        Robot.driveMoter(1, 0)
        Robot.driveMoter(4, 0)
        # Determine path closest to center with no obstacle
        centerHeading = possibleHeadings.pop(self, int(len(possibleHeadings) / 2))[0]
        inLoop = true
        while (inLoop):
            middleHeading = int(len(possibleHeadings) / 2)
            tempHeading = possibleHeadings.pop(self, middleHeading)
            # Check for next value to the right of center
            if (not tempHeading[1]):
                return tempHeading[0]
            if(tempHeading[0] is None):
                inLoop = false
            tempHeading = possibleHeadings.pop(self, middleHeading -1)
            # Check for next vale to the left of center
            if (not tempHeading[1]):
                return tempHeading[0]
            if __name__ == '__main__':
                if (tempHeading[0] is None):
                    inLoop = false
        # If all scanned values have something in the way then ...
        # TO BE CONTINUED

