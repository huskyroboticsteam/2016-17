from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle
from random import random
from path_finding import find_path


def str_to_tuple_of_float(s):
    a = s.split(' ')
    return (float(a[0]), float(a[1]))


def main():
    #start = str_to_tuple_of_float(raw_input('start (x, y with spaces in between): '))
    #target = str_to_tuple_of_float(raw_input('target (x, y with spaces in between): '))
    #n = int(raw_input('number of obstacles: '))
    #obstacles = []
    #for _ in range(n):
    #    obstacles.append(str_to_tuple_of_float(raw_input('Obstacle: ')))
    #buffer_width = float(raw_input('Buffer width: '))

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
    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]
        l = Line2D([a[0], b[0]], [a[1], b[1]], color='black')
        ax.add_line(l)
    for obs in obstacles:
        ax.add_patch(Circle(obs, buffer_width))
    ax.add_patch(Circle(start, 0.01, color='red'))
    ax.add_patch(Circle(target, 0.01, color='red'))

    ax.autoscale(enable=True)
    ax.set_aspect('equal')

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure("path.png")


if __name__ == '__main__':
    main()
