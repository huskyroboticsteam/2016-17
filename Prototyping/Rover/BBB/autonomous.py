from path_finding import find_path
from path_following import PathFollower
from Utils import distance


class Autonomous:
    """
    Plans and follows paths to avoid obstacles.
    All coordinates are in meters
    Attributes:
        target (tuple of (float, float) or None): coordinate of target.
        obstacles (list of tuple of (float, float)): coordinates of currently known obstacles.
        ignore_obstacle_distance (float): If a newly detected obstacle is this near to an obstacle used for planning
            the current path, then it will be ignored until the path is re-planned. (In meters)
        obstacles_for_curr_path (list of tuple of (float, float)): the obstacles used for planning the current path
        path (list of tuple of (float, float)): The currently planned path. "None" if not calculated yet.
        path_follower (PathFollower): Object for managing path-following state.
    """
    def __init__(self, path=None):
        """
        Args:
            target (tuple of (float, float)): The target x, y coordinates
        """
        self.target = None
        self.obstacles = []
        self.ignore_obstacle_distance = 0.1
        self.obstacles_for_curr_path = []
        self.path = path
        self.path_follower = PathFollower(self.path)

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
        self.obstacles.append(coord)
        # Re-plan path if the new obstacle is sufficiently far from the obstacles already used for planning the path
        if self.path is not None:
            for obs in self.obstacles_for_curr_path:
                if distance(coord, obs) > self.ignore_obstacle_distance:
                    self.path = None
                    return

    def clear_all_obstacles(self):
        """
        Resets the state. Forgets about all known obstacles.
        """
        self.obstacles = []
        self.obstacles_for_curr_path = []
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
        assert self.target is not None
        self._refresh_path(location)
        assert not self.is_done(location)
        return self.path_follower.go(location, heading)

    def is_done(self, location):
        """
        Returns (bool): whether the robot has reached the destination yet
        """
        if self.target is None:
            return True
        self._refresh_path(location)
        done =  self.path_follower.is_done(location)
        if done:
            self.target = None
        return done

    def _refresh_path(self, location):
        """
        Calculates the path and resets the state if necessary.
        Internal use only.
        Args:
            location (tuple of (float, float)): Current location x, y
        """
        assert self.target is not None
        if self.path is None:
            self.path = find_path(location, self.target, self.obstacles)
            self.path_follower.set_path(self.path)
            self.obstacles_for_curr_path = self.obstacles
