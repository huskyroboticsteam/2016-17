from math import radians, sin, cos
from random import random
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle

from path_following import PathFollower
from path_finding import find_path
from Utils import normalize_angle


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
