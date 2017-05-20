from math import hypot, atan2, degrees
from PID import PID 
from Utils import normalize_angle
import Utils

# Set this to True to ignore the heading parameter in the go() method.
# If it is set to True, will try to guess headings based on GPS changes.
# For use in case the magnetometer is broken.
IGNORE_HEADING = False


class PathFollower:
    """
    Uses a PID loop to steer the robot to follow a path.
    Used by autonomous.py
    Attributes:
        path (list of tuple of (float, float)): The list of current destinations to go to.
        pid (PID): The PID controller for the angle
        position_epsilon(float): How close in METERS the robot has to be for a destination to be considered reached
    Attributes used if IGNORE_HEADING is True:
        prev_location (tuple of (float, float)): Last recorded GPS location
        prev_heading (float): Last known/guessed heading
    """
    def __init__(self):
        self.path = []
        # TODO fine tune this
        self.pid = PID(0.5, 0.0, 0.0)
        self.pid.setTarget(0.0)
        self.position_epsilon = 3

        # logging info:
        open('path_log.txt', 'w').close()

        # Used if IGNORE_HEADING is True
        self.prev_location = None
        self.prev_heading = 0.0

    def go(self, location, heading):
        """
        Args:
            location (tuple of (float, float)): The current GPS coordinates of the robot.
            heading (float): The current heading of the robot.
                (0.0 for north, 90.0 for east, 180.0 for south, 270.0 for west)
        Returns (float): The turn value of the robot. 100 is full right. -100 is full left. 0 is straight.
        """
        assert not self.is_done(location)
        self._remove_reached_destinations(location)
        assert self.path != []
        '''
        dest = self.path[0]
        dx = dest[0] - location[0]
        dy = dest[1] - location[1]
        desired_heading = normalize_angle(90.0 - degrees(atan2(dy, dx)))
        diff_angle = no rmalize_angle(heading - desired_heading)
        if diff_angle > 180.0:
            diff_angle -= 360.0
        self.pid.run(diff_angle)
        print dx, dy, heading, desired_heading, self.pid.getOutput()
        turn = min(max(self.pid.getOutput(), -100.0), 100.0)
        print 'PathFollower: go() returning ' + str(turn)
        '''
        if IGNORE_HEADING:
            self._update_heading(location)
            heading = self.prev_heading
        # updates made by Brian 5/18/17
        # uses new distance code in Utils
        # get the heading between cur location and first in path
        desired_heading = Utils.bearing(location, self.path[0])
        # use PID to get the turn value from desired heading
        self.pid.run(heading - desired_heading)
        print "desired heading: " + str(desired_heading)
        print "cur heading: " + str(heading)
        print "desired location: " + str(self.path[0])
        print "cur location: " + str(location)

        turn = min(max(self.pid.getOutput(), -100.0), 100.0)

        return turn

    def is_done(self, location):
        """
        Returns (bool): whether the robot has reached the final destination yet
        """
        if IGNORE_HEADING:
            self._update_heading(location)
        self._remove_reached_destinations(location)
        return self.path == []

    def set_path(self, path):
        """
        Sets the path
        Args:
            path (list of tuple of (float, float))
        """
        self.path = path
        self.pid.reset()
        self.pid.setTarget(0.0)

    def _remove_reached_destinations(self, location):
        """
        Internal use only
        """
        while self.path != [] and Utils.dist(self.path[0], location) <= self.position_epsilon:
            del self.path[0]
            self.pid.reset()
            self.pid.setTarget(0.0)
        print 'Current position: ' + str(location)
        print 'Destinations' + str(self.path)
        if self.path == []:
            print 'At destination'
        else:
            with open("path_log.txt", "a") as myfile:
                myfile.write("Distance:" + str(Utils.dist(self.path[0], location)) + '\n')
            print 'Distance to destination: ' + str(Utils.dist(self.path[0], location))

    def _update_heading(self, location):
        """
        Internal use only.
        Used to update prev_location and prev_heading if IGNORE_HEADING is True
        Args:
            location (tuple of (float, float)): current coordinates
        """
        if self.prev_location is None:
            self.prev_location = location
        elif self.prev_location != location:
            self.prev_heading = Utils.bearing(self.prev_location, location)
            self.prev_location = location
