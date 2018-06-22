from reconstruction import Polygon
import matplotlib.pyplot as plt
from collections import namedtuple
import sys


def main(expression, bounds, seg_length):
    p = Polygon(expression, bounds, seg_length)
    pts = p.get_pts()
    triangles = earclip(pts)
    for t in triangles:
        plt.plot([t[0][0], t[1][0]], [t[0][1],t[1][1]])
        plt.plot([t[1][0], t[2][0]], [t[1][1], t[2][1]])
        plt.plot([t[2][0], t[0][0]], [t[2][1],t[0][1]])
    plt.show()
    return


Point = namedtuple('Point', ['x', 'y'])    #STRUCTURE defining a point

def earclip(polygon):
    ear_vertex = []
    triangles = []
    polygon = [Point(*point) for point in polygon]

    # Writing this function here for more generalized implementation. Not required for this project as the returned points are counter clockwise.
    if _is_clockwise(polygon):
        polygon.reverse()

    point_count = len(polygon)
    for i in range(point_count):
        prev_index = i - 1
        prev_point = polygon[prev_index]
        point = polygon[i]
        next_index = (i + 1) % point_count
        next_point = polygon[next_index]

        if _is_ear(prev_point, point, next_point, polygon):
            ear_vertex.append(point)

    while ear_vertex and point_count >= 3:
        ear = ear_vertex.pop(0)
        i = polygon.index(ear)
        prev_index = i - 1
        prev_point = polygon[prev_index]
        next_index = (i + 1) % point_count
        next_point = polygon[next_index]
        polygon.remove(ear)
        point_count -= 1
        triangles.append(((prev_point.x, prev_point.y), (ear.x, ear.y), (next_point.x, next_point.y)))
        if point_count > 3:
            prev_prev_point = polygon[prev_index - 1]
            next_next_index = (i + 1) % point_count
            next_next_point = polygon[next_next_index]
            groups = [
                (prev_prev_point, prev_point, next_point, polygon),
                (prev_point, next_point, next_next_point, polygon)
            ]
            for group in groups:  #This part makes it seem like O(N^3) algorithm but it is O(N^2) in reality
                p = group[1]
                if _is_ear(*group):
                    if p not in ear_vertex:
                        ear_vertex.append(p)
                elif p in ear_vertex:
                    ear_vertex.remove(p)
    return triangles


def _is_clockwise(polygon):
    s = 0
    polygon_count = len(polygon)
    for i in range(polygon_count):
        point = polygon[i]
        point2 = polygon[(i + 1) % polygon_count]
        s += (point2.x - point.x) * (point2.y + point.y)
    return s > 0


def _is_convex(prev, point, next):
    return _triangle_sum(prev.x, prev.y, point.x, point.y, next.x, next.y) < 0


def _is_ear(p1, p2, p3, polygon):
    ear = _contains_no_points(p1, p2, p3, polygon) and \
            _is_convex(p1, p2, p3) and \
            _triangle_area(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y) > 0
    return ear


def _contains_no_points(p1, p2, p3, polygon):
    for pn in polygon:
        if pn in (p1, p2, p3):
            continue
        elif _is_point_inside(pn, p1, p2, p3):
            return False
    return True


def _is_point_inside(p, a, b, c):
    area = _triangle_area(a.x, a.y, b.x, b.y, c.x, c.y)
    area1 = _triangle_area(p.x, p.y, b.x, b.y, c.x, c.y)
    area2 = _triangle_area(p.x, p.y, a.x, a.y, c.x, c.y)
    area3 = _triangle_area(p.x, p.y, a.x, a.y, b.x, b.y)
    return area == sum([area1, area2, area3])


def _triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def _triangle_sum(x1, y1, x2, y2, x3, y3):
    return x1 * (y3 - y2) + x2 * (y1 - y3) + x3 * (y2 - y1)


if __name__ == "__main__":
    """Read the input given thought the file"""
    point_file = open(sys.argv[1], "r")
    #point_file = open("expression-1.txt", "r")
    lines = []
    for line in point_file:
        lines.append(str(line))
    expression = lines[0]
    Bounds_str = lines[1].split(",")
    bounds = []
    for bound in Bounds_str:
        bounds.append(int(bound))
    seg_length = int(lines[2])
    main(expression, bounds, seg_length)