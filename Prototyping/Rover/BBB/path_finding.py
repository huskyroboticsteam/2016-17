from shapely.geometry import Point, Polygon, MultiPolygon, LinearRing
from shapely.ops import cascaded_union
import pyvisgraph as vg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Circle
from random import random

# TODO: fix case with start/target inside the obstacles
# http://stackoverflow.com/questions/33311616/find-coordinate-of-closest-point-on-polygon-shapely

# TODO: Steer rover to follow this line.
# Maybe use PID loop?


def find_path(start, target, obstacles, buffer_width):
    """
    Finds a path from one point to another while not getting near obstacles
    Assumes that the actual start and target points are outside of obstacles, but the values given might be inaccurate.
    Args:
        start, target (tuple of (float, float)): starting points and target points
        obstacles (list of tuple of (float, float)): list of obstacles
        buffer_width (float): Do not go this near to the obstacles
    Returns (list of tuple of (float, float)): The path.
    """
    polygon_list = [Point(a).buffer(buffer_width, resolution=3) for a in obstacles]
    union_all = cascaded_union(polygon_list)
    if isinstance(union_all, Polygon):
        union_all = MultiPolygon([union_all])
    start_outside = list(nearest_outside(Point(start), union_all).coords)[0]
    target_outside = list(nearest_outside(Point(target), union_all).coords)[0]
    boundary_list = [[vg.Point(b[0], b[1]) for b in a.exterior.coords] for a in union_all]
    for i in range(len(boundary_list)):
        del boundary_list[i][-1]
    g = vg.VisGraph()
    g.build(boundary_list)
    shortest = g.shortest_path(
        vg.Point(start_outside[0], start_outside[1]),
        vg.Point(target_outside[0], target_outside[1]))
    return [(a.x, a.y) for a in shortest]


def nearest_outside(p, area, epsilon = 0.00001):
    """
    Finds the point closest to point p that is outside of the area and at least epsilon away from it.
    Assumes that the area doesn't have holes.
    Args:
        p (Point): The point
        area (MultiPolygon or Polygon): the area
    Returns (Point): the desired point
    """
    area = area.buffer(epsilon)
    if not area.contains(p):
        return p
    poly = [a for a in MultiPolygon(area) if a.contains(p)][0]
    assert poly.contains(p)
    poly_ext = LinearRing(poly.exterior.coords)
    d = poly_ext.project(p)
    return poly_ext.interpolate(d)


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
