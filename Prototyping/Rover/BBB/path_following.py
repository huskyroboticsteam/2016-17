from math import hypot, atan2, degrees
from PID import PID 
from Utils import normalize_angle

class PathFollower:
    """
    Uses a PID loop to steer the robot to follow a path.
    Used by autonomous.py
    Attributes:
        path (list of tuple of (float, float)): The list of current destinations to go to.
        pid (PID): The PID controller for the angle
        position_epsilon(float): How close the robot has to be for a destination to be considered reached
    """
    def __init__(self):
        self.path = []
        # TODO fine tune this
        self.pid = PID(0.5, 0.0, 0.0)
        self.pid.setTarget(0.0)
        self.position_epsilon = 0.05

    def go(self, location, heading):
        """
        Args:
            location (tuple of (float, float)): The current x, y coordinates of the robot.
            heading (float): The current heading of the robot.
                (0.0 for north, 90.0 for east, 180.0 for south, 270.0 for west)
        Returns (float): The turn value of the robot. 100 is full right. -100 is full left. 0 is straight.
        """
        assert not self.is_done(location)
        self._remove_reached_destinations(location)
        assert self.path != []
        dest = self.path[0]
        dx = dest[0] - location[0]
        dy = dest[1] - location[1]
        desired_heading = normalize_angle(90.0 - degrees(atan2(dy, dx)))
        diff_angle = normalize_angle(heading - desired_heading)
        if diff_angle > 180.0:
            diff_angle -= 360.0
        self.pid.run(diff_angle)
        print dx, dy, heading, desired_heading, self.pid.getOutput()
        return min(max(self.pid.getOutput(), -100.0), 100.0)

    def is_done(self, location):
        """
        Returns (bool): whether the robot has reached the final destination yet
        """
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
        while self.path != [] and \
                        hypot(self.path[0][0] - location[0], self.path[0][1] - location[1]) <= self.position_epsilon:
            del self.path[0]
            self.pid.reset()
            self.pid.setTarget(0.0)
