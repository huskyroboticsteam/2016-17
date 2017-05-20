from shapely.geometry import Point, Polygon, MultiPolygon, LinearRing
from shapely.ops import cascaded_union
import pyvisgraph as vg


def find_path(start, target, obstacles, buffer_width=0.1):
    """
    Finds a path from one point to another while not getting near obstacles
    Assumes that the actual start and target points are outside of obstacles, but the values given might be inaccurate.
    Used by autonomous.py
    Args:
        start, target (tuple of (float, float)): starting points and target points
        obstacles (list of tuple of (float, float)): list of obstacles
        buffer_width (float): How far must the center of the robot be from detected obstacles.
    Returns (list of tuple of (float, float)): The path as a list of coordinates. Does not include the starting point
        but includes the ending point.
    """
    polygon_list = [Point(a).buffer(buffer_width, resolution=3) for a in obstacles]
    union_all = cascaded_union(polygon_list)
    if isinstance(union_all, Polygon):
        union_all = to_multi_polygon([union_all])
    start_outside = list(_nearest_outside(Point(start), union_all).coords)[0]
    target_outside = list(_nearest_outside(Point(target), union_all).coords)[0]
    boundary_list = [[vg.Point(b[0], b[1]) for b in a.exterior.coords] for a in union_all]
    for i in range(len(boundary_list)):
        del boundary_list[i][-1]
    g = vg.VisGraph()
    g.build(boundary_list)
    shortest = g.shortest_path(
        vg.Point(start_outside[0], start_outside[1]),
        vg.Point(target_outside[0], target_outside[1]))
    path = [(a.x, a.y) for a in shortest]
    while path != [] and path[0] == start:
        del path[0]
    if path == [] or path[-1] != target:
        path.append(target)
    return path


def _nearest_outside(p, area, epsilon=0.00001):
    """
    Finds the point closest to point p that is outside of the area and at least epsilon away from it.
    Assumes that the area doesn't have holes.
    Internal use only.
    Args:
        p (Point): The point
        area (MultiPolygon or Polygon): the area
    Returns (Point): the desired point
    """
    area = area.buffer(epsilon)
    if not area.contains(p):
        return p
    poly = [a for a in to_multi_polygon(area) if a.contains(p)][0]
    assert poly.contains(p)
    poly_ext = LinearRing(poly.exterior.coords)
    d = poly_ext.project(p)
    return poly_ext.interpolate(d)

def to_multi_polygon(a):
    """
    Converts a Polygon or a MultiPolygon to a MultiPolygon
    """
    if isinstance(a, MultiPolygon):
        return a
    elif isinstance(a, Polygon):
        return MultiPolygon([a])
    else:
        assert False
