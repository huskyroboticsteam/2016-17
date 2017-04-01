from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import cascaded_union
import pyvisgraph as vg

def find_path(start, target, obstacles, buffer_width):
    """
    Finds a path from one point to another while not getting near obstacles
    Args:
        start, target (tuple of (float, float)): starting points and target points
        obstacles (list of tuple of (float, float)): list of obstacles
        buffer_width (float): Do not go this near to the obstacles
    Returns (list of tuple of (float, float)): The path
    """
    polygon_list = [Point(a).buffer(buffer_width) for a in obstacles]
    union_all = cascaded_union(polygon_list)
    if isinstance(union_all, Polygon):
        union_all = MultiPolygon([union_all])
    boundary_list = [[vg.Point(b[0], b[1]) for b in a.exterior.coords] for a in union_all]
    g = vg.VisGraph()
    g.build(boundary_list)
    shortest = g.shortest_path(vg.Point(start[0], start[1]), vg.Point(target[0], target[1]))
    return [(a.x, a.y) for a in shortest]


def str_to_tuple_of_float(s):
    a = s.split(' ')
    return (float(a[0]), float(a[1]))


def main():
    start = str_to_tuple_of_float(raw_input('start (x, y with spaces in between): '))
    target = str_to_tuple_of_float(raw_input('target (x, y with spaces in between): '))
    n = int(raw_input('number of obstacles: '))
    obstacles = []
    for _ in range(n):
        obstacles.append(str_to_tuple_of_float(raw_input('Obstacle: ')))
    buffer_width = float(raw_input('Buffer width: '))
    print find_path(start, target, obstacles, buffer_width)


if __name__ == '__main__':
    main()
