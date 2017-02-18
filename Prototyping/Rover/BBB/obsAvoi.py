import Robot

class obsAvoi :
# Obstacle Avoidance
# A work in progress
# Will be moved over to Navigation.py


    def __init__(self, LP, RP):
        self.POT_LEFT = LP
        self.POT_RIGHT = RP
        self.POT_MIDDLE = (self.POT_LEFT + self.POT_RIGHT) / 2

    # TODO: Return bool signifying if there is obstacle witin given distance
    #       Waiting for code from science sub-team
    def isObstacle (self, distance):
        return false

    # Looks around for obstacles and returns a heading without obstacle
    def getDetourHeading(self):
        possibleHeadings = []
        # Stop the rover
        for i in range(1, 5):
            robot.driveMotor(i, 0)
        # Make the rover look as far left as possible
        while(readPot < POT_LEFT):
            robot.driveMotor(1, 20)
            robot.driveMotor(2, -20)
            robot.driveMotor(3, -20)
            robot.driveMotor(4, 20)
        robot.driveMotor(1, 0)
        robot.driveMotor(2, 0)
        robot.driveMotor(3, 0)
        robot.driveMotor(4, 0)
        # Look from left to right gathering obstacles in an arc ahead
        while(readPot > POT_Right):
            robot.driveMoter(1, -20)
            robot.driveMoter(2, 20)
            robot.driveMoter(3, 20)
            robot.driveMoter(4, -20)
            possibleHeadings.append((getMag(), isObstacle(self, 2)))
            #TODO: Maybe? Add pause to slow read speed
        Robot.driveMoter(1, 0)
        robot.driveMoter(2, 0)
        robot.driveMoter(3, 0)
        Robot.driveMoter(4, 0)
        centerHeading = possibleHeadings.pop(self, int(len(possibleHeadings) / 2))[0]
        # Determine path closest to center with no obstacle
        # Removes values from center of array outward
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
            # Check for next value to the left of center
            if (not tempHeading[1]):
                return tempHeading[0]
            if (tempHeading[0] is None):
                inLoop = false
        # If all scanned values have something in the way then ...
        # TODO Fix that problem
        # TO BE CONTINUED

