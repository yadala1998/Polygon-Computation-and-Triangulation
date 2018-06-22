from collections import namedtuple
import sys
from reconstruction import Polygon
import numpy as np
import warnings

Pt = namedtuple('Pt', 'x, y')  # Point
Edge = namedtuple('Edge', 'a, b')  # Polygon edge from a to b
Poly = namedtuple('Poly', 'name, edges')  # Polygon

_eps = 0.00001
_huge = sys.float_info.max
_tiny = sys.float_info.min


def rayintersectseg(p, edge):
    a, b = edge
    if a.y > b.y:
        a, b = b, a
    if p.y == a.y or p.y == b.y:
        p = Pt(p.x, p.y + _eps)
    intersect = False
    if (p.y > b.y or p.y < a.y) or (
            p.x > max(a.x, b.x)):
        return False
    if p.x < min(a.x, b.x):
        intersect = True
    else:
        if abs(a.x - b.x) > _tiny:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _huge
        if abs(a.x - p.x) > _tiny:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _huge
        intersect = m_blue >= m_red
    return intersect


def odd(x):
    return x % 2 == 1


def ispointinside(p, poly):
    return odd(sum(rayintersectseg(p, edge)
                    for edge in poly.edges))

def polypp(poly):
    print ("\n  Polygon(name='%s', edges=(" % poly.name)
    print ('   ', ',\n    '.join(str(e) for e in poly.edges) + '\n    ))')

def point_to_line_dist(point, line):
    # unit vector
    unit_line = line[1] - line[0]
    norm_unit_line = unit_line / np.linalg.norm(unit_line)
    warnings.filterwarnings("ignore")
    # compute the perpendicular distance to the theoretical infinite line
    segment_dist = (
        np.linalg.norm(np.cross(line[1] - line[0], line[0] - point)) /
        np.linalg.norm(unit_line)
    )
    warnings.filterwarnings("ignore")
    diff = (
        (norm_unit_line[0] * (point[0] - line[0][0])) +
        (norm_unit_line[1] * (point[1] - line[0][1]))
    )

    x_seg = (norm_unit_line[0] * diff) + line[0][0]
    y_seg = (norm_unit_line[1] * diff) + line[0][1]

    endpoint_dist = min(
        np.linalg.norm(line[0] - point),
        np.linalg.norm(line[1] - point)
    )

    # decide if the intersection point falls on the line segment
    lp1_x = line[0][0]  # line point 1 x
    lp1_y = line[0][1]  # line point 1 y
    lp2_x = line[1][0]  # line point 2 x
    lp2_y = line[1][1]  # line point 2 y
    is_betw_x = lp1_x <= x_seg <= lp2_x or lp2_x <= x_seg <= lp1_x
    is_betw_y = lp1_y <= y_seg <= lp2_y or lp2_y <= y_seg <= lp1_y
    if is_betw_x and is_betw_y:
        return segment_dist
    else:
        # if not, then return the minimum distance to the segment endpoints
        return endpoint_dist

if __name__ == '__main__':
    """Reading Polygon Inputs"""
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
    """Reading Points file"""
    point_file = open(sys.argv[2], "r")
    #point_file = open("points-1-3.txt", "r")
    points = []
    for row in point_file:
        strings = row.split()
        points.append(Pt(x = float(strings[0]), y = float(strings[1])))

    """Making a Polygon"""
    p = Polygon(expression, bounds, seg_length)
    pts = p.get_pts()
    all_points = []
    all_edges = []
    all_edges_np = []
    for pt in pts:
        temp_pt = Pt(x = pt[0],y = pt[1])
        all_points.append(temp_pt)
    for i in range(0, len(all_points)):
        pt1 = all_points[i%len(all_points)]
        pt2 = all_points[(i+1)%len(all_points)]
        all_edges.append(Edge(a = pt1, b = pt2))
    for i in range(0, len(pts)):
        all_edges_np.append(np.array([pts[i%len(pts)], pts[(i+1)%len(pts)]]))
    #Find the shortest distance
    distances = []
    for point in points:
        dist = sys.float_info.max
        for edge in all_edges_np:
            if point_to_line_dist(np.array([point.x,point.y]), edge) < dist:
                dist = point_to_line_dist(np.array([point.x,point.y]), edge)
        distances.append(dist)

    polygon_temp = Poly(name = 'Current Polygon', edges = tuple(all_edges))
    counter = 0
    for point in points:
        print("(" + str(point.x) + str(point.y) + ")" + " : " + "in = " + str(ispointinside(point, polygon_temp)) +  ", distance =" + str(distances[counter]))
        counter = counter + 1

