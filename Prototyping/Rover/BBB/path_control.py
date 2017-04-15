from path_finding import find_path
from path_following import PathFollower

# TODO: Integrate this code into main code.


class PathControl:
    """
    Plans and follows paths to avoid obstacles.
    Attributes:
        target (tuple of (float, float)): (x, y) coordinate of target.
        obstacles (list of tuple of (float, float)): (x, y) locations of currently known obstacles.
        buffer_width (float): How far must the center of the robot be from detected obstacles.
        path (list of tuple of (float, float)): The currently planned path. "None" if not calculated yet.
        path_follower (PathFollower): Object for managing path-following state.
    """
    def __init__(self, target, buffer_width=0.1):
        """
        Args:
            target (tuple of (float, float)): The target x, y coordinates
        """
        self.target = target
        self.obstacles = []
        self.buffer_width = buffer_width
        self.path = None
        self.path_follower = PathFollower()

    def set_target(self, target):
        """
        Args
            target (tuple of (float, float)): The target x, y coordinates
        """
        self.target = target

    def add_obstacle(self, coord):
        """
        Adds an obstacle to the list.
        Args:
            coord (tuple of (float, float)): The x, y coordinates of the obstacle.
        """
        # TODO: Maybe ignore obstacles that are near known obstacles?
        self.obstacles.append(coord)
        self.path = None

    def clear_all_obstacles(self):
        """
        Resets the state. Forgets about all known obstacles.
        """
        self.obstacles = []
        self.path = None

    def go(self, location, heading):
        """
        Finds how much the robot should turn. Assumes that the robot always moves forward.
        Should be called periodically.
        Args:
            location (tuple of (float, float)): The current x, y coordinates of the robot.
            heading (float): The current heading of the robot.
                (0.0 for north, 90.0 for east, 180.0 for south, 270.0 for west)
        Returns (float): The turn value of the robot. 100 is full right. -100 is full left. 0 is straight.
        """
        self._refresh_path(location)
        assert not self.is_done(location)
        return self.path_follower.go(location, heading)

    def is_done(self, location):
        """
        Returns (bool): whether the robot has reached the destination yet
        """
        self._refresh_path(location)
        return self.path_follower.is_done(location)

    def _refresh_path(self, location):
        """
        Calculates the path and resets the state if necessary.
        Internal use only.
        Args:
            location (tuple of (float, float)): Current location x, y
        """
        if self.path is None:
            self.path = find_path(location, self.target, self.obstacles, self.buffer_width)
            self.path_follower.set_path(self.path)
