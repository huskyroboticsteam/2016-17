from math import hypot, atan2, degrees, radians, sin, cos
from path_finding import find_path
from PID import PID
from Utils import normalize_angle

from random import random
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle

class PathFollower:
    """
    Uses a PID loop to steer the robot to follow a path.
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
        self.remove_reached_destinations(location)
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
        self.remove_reached_destinations(location)
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

    def remove_reached_destinations(self, location):
        while self.path != [] and \
                hypot(self.path[0][0] - location[0], self.path[0][1] - location[1]) <= self.position_epsilon:
            del self.path[0]
            self.pid.reset()
            self.pid.setTarget(0.0)


def main():
    start = (random(), random())
    target = (random(), random())
    n = 20
    obstacles = []
    for _ in range(n):
        obstacles.append((random(), random()))
    buffer_width = 0.1

    path = find_path(start, target, obstacles, buffer_width)
    print path

    fig = Figure(figsize=[4, 4])
    ax = Axes(fig, [.1,.1,.8,.8])
    fig.add_axes(ax)
    for obs in obstacles:
        ax.add_patch(Circle(obs, buffer_width))
    ax.add_patch(Circle(start, 0.01, color='red'))
    ax.add_patch(Circle(target, 0.01, color='red'))

    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]
        l = Line2D([a[0], b[0]], [a[1], b[1]], color='black')
        ax.add_line(l)

    location = start
    heading = random() * 360.0
    path_follower = PathFollower()
    path_follower.set_path(path)
    while not path_follower.is_done(location):
        ax.add_patch(Circle(location, 0.01, color='black'))
        turn = path_follower.go(location, heading)
        heading = normalize_angle(heading + turn * 0.2)
        angle_to_x = radians(90.0 - heading)
        step = 0.01
        dx = step * cos(angle_to_x)
        dy = step * sin(angle_to_x)
        location = (location[0] + dx, location[1] + dy)

        #ax.autoscale(enable=True)
        #ax.set_aspect('equal')
        #canvas = FigureCanvasAgg(fig)
        #canvas.print_figure("path_following_test_output.png")

    ax.autoscale(enable=True)
    ax.set_aspect('equal')
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure("path_following_test_output.png")

if __name__ == '__main__':
    main()
