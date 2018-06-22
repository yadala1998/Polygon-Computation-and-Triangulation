import sys
import numpy
import matplotlib.pyplot as plt
from enum import Enum

class Polygon(object):

    def __init__(self,expression, bounds, seg_length):
        self.pts = main(expression, bounds, seg_length)

    def get_pts(self):
        return self.pts


def main(expression, bounds, seg_length):

    class Cell(object):
        def __init__(self, cell_rel_pos, center, expression):
            self.cell_pos = cell_rel_pos
            self.center = center
            self.corners = [[round(center[0] - hs, 3), round(center[1] + hs, 3)],
                            [round(center[0] + hs, 3), round(center[1] + hs, 3)],
                            [round(center[0] + hs, 3), round(center[1] - hs, 3)],
                            [round(center[0] - hs, 3), round(center[1] - hs, 3)]]
            self.expression = expression
            self.binary_Index = []
            for pt in self.corners:
                x = pt[0]
                y = pt[1]
                corner_value = eval(self.expression)
                if corner_value < 0:
                    self.binary_Index.append(0)
                elif corner_value >= 0:
                    self.binary_Index.append(1)

        def get_cell_pos(self):
            return self.cell_pos

        def get_center(self):
            return self.center

        def get_corners(self):
            return self.corners

        def get_binary_Index(self):
            return self.binary_Index

    class IndexCases(Enum):
        case_0 = [0, 0, 0, 0]
        case_1 = [0, 0, 0, 1]
        case_2 = [0, 0, 1, 0]
        case_3 = [0, 0, 1, 1]
        case_4 = [0, 1, 0, 0]
        case_5 = [0, 1, 0, 1]
        case_6 = [0, 1, 1, 0]
        case_7 = [0, 1, 1, 1]
        case_8 = [1, 0, 0, 0]
        case_9 = [1, 0, 0, 1]
        case_10 = [1, 0, 1, 0]
        case_11 = [1, 0, 1, 1]
        case_12 = [1, 1, 0, 0]
        case_13 = [1, 1, 0, 1]
        case_14 = [1, 1, 1, 0]
        case_15 = [1, 1, 1, 1]

    """Getting Input from the file that defines the expression, the bounds and maximum segment length"""
    boundsOfFile = bounds
    x_min = boundsOfFile[0]
    x_max = boundsOfFile[1]
    y_min = boundsOfFile[2]
    y_max = boundsOfFile[3]
    h = seg_length
    all_segments = []

    """Max Cell dimensions"""
    hs = round(h * (2 ** .5) / 4, 3)

    """Find the grid intervals in x,y"""
    num_Of_x = int((x_max - x_min) / (2 * hs) - 1)
    num_Of_y = int((y_max - y_min) / (2 * hs) - 1)
    xGrid = []
    for i in range(0, num_Of_x + 1):
        if i == 0:
            xGrid.append(round(x_min + hs, 3))
        elif i == num_Of_x + 1:
            xGrid.append(round(x_max - hs, 3))
        else:
            xGrid.append(round(x_min + hs + (hs * 2) * i, 3))
    yGrid = []
    for j in range(0, num_Of_y + 1):
        if j == 0:
            yGrid.append(round(y_min + hs, 3))
        elif j == num_Of_y + 1:
            yGrid.append(round(y_max - hs, 3))
        else:
            yGrid.append(round(y_min + hs + (hs * 2) * j, 3))

    """Creating Cells with the grids obtained"""
    cells = []
    xRelativePos = 0
    for x in xGrid:
        yRelativePos = 0
        for y in yGrid:
            pos = (round(x, 3), round(y, 3))
            d = {'x': pos[0], 'y': pos[1]}
            cell_pos = (xRelativePos, yRelativePos)
            plt.plot([x - hs, x - hs], [y + hs, y - hs], color='black')
            plt.plot([x + hs, x + hs], [y + hs, y - hs], color='black')
            plt.plot([x + hs, x - hs], [y + hs, y + hs], color='black')
            plt.plot([x + hs, x - hs], [y - hs, y - hs], color='black')
            f_value = eval(expression,d)
            if f_value >= 0:
                plt.scatter(x, y, color="blue", s=10)
            else:
                plt.scatter(x, y, color="red", s=5)
            cells.append(Cell(cell_pos, pos, expression))
            yRelativePos = yRelativePos + 1
        xRelativePos = xRelativePos + 1

    """Formulae for linear interpolation"""
    def interpolateRight(right_top, right_bottom, right_top_val, right_bottom_val):
        y = right_top[1] + (right_bottom[1] - right_top[1]) * (0 - right_top_val) / (right_bottom_val - right_top_val)
        x = right_bottom[0]
        return round(x, 3), round(y, 3)

    def interpolateLeft(left_top, left_bottom, left_top_val, left_bottom_val):
        y = left_top[1] + (left_bottom[1] - left_top[1]) * (0 - left_top_val) / (left_bottom_val - left_top_val)
        x = left_bottom[0]
        return round(x, 3), round(y, 3)

    def interpolateTop(top_left, top_right, top_left_val, top_right_val):
        x = top_right[0] + (top_left[0] - top_right[0]) * (0 - top_right_val) / (top_left_val - top_right_val)
        y = top_left[1]
        return round(x, 3), round(y, 3)

    def interpolateBottom(bottom_left, bottom_right, bottom_left_val, bottom_right_val):
        x = bottom_right[0] + (bottom_left[0] - bottom_right[0]) * (0 - bottom_right_val) / (bottom_left_val - bottom_right_val)
        y = bottom_left[1]
        return round(x, 3), round(y, 3)

    """Iterating throught the cells to perform marching squares"""
    for cell in cells:
        center = cell.get_center()
        x = center[0]
        y = center[1]
        index = cell.get_binary_Index()
        corners = cell.get_corners()
        topLeftPoint = corners[0]
        topRightPoint = corners[1]
        bottomRightPoint = corners[2]
        bottomLeftPoint = corners[3]


        if numpy.array_equal(IndexCases.case_1.value, index):
            """Compute the points"""
            d1 = {'x': topLeftPoint[0], 'y': y + hs}
            d2 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d1)
            valueOfLeftBottom = eval(expression, d2)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)

            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_2.value, index):
            """Compute the points"""
            d1 = {'x': topRightPoint[0], 'y': y + hs}
            d2 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d1)
            valueOfRightBottom = eval(expression, d2)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_3.value, index):
            """Compute the points"""
            d1 = {'x': topLeftPoint[0], 'y': y + hs}
            d2 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d1)
            valueOfLeftBottom = eval(expression, d2)
            vert_zero_left = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)

            d3 = {'x': topRightPoint[0], 'y': y + hs}
            d4 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d3)
            valueOfRightBottom = eval(expression, d4)
            vert_zero_right = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            """Append the points"""
            pt1 = ([vert_zero_left[0], vert_zero_left[1]])
            pt2 = ([vert_zero_right[0], vert_zero_right[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_4.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)

            d3 = {'x': topRightPoint[0], 'y': y + hs}
            d4 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d3)
            valueOfRightBottom = eval(expression, d4)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_5.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': topLeftPoint[0], 'y': y + hs}
            d4 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d3)
            valueOfLeftBottom = eval(expression, d4)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)


            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])


            d5 = {'x': topRightPoint[0], 'y': y + hs}
            d6 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d5)
            valueOfRightBottom = eval(expression, d6)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)


            d7 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d8 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d7)
            valueOfBottomRight = eval(expression, d8)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt3 = ([horz_zero[0], horz_zero[1]])
            pt4 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])
            all_segments .append([pt3, pt4])


        elif numpy.array_equal(IndexCases.case_6.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero_top = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero_bot = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero_top[0], horz_zero_top[1]])
            pt2 = ([horz_zero_bot[0], horz_zero_bot[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_7.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': topLeftPoint[0], 'y': y + hs}
            d4 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d3)
            valueOfLeftBottom = eval(expression, d4)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_8.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': topLeftPoint[0], 'y': y + hs}
            d4 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d3)
            valueOfLeftBottom = eval(expression, d4)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_9.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero_top = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero_bot = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero_top[0], horz_zero_top[1]])
            pt2 = ([horz_zero_bot[0], horz_zero_bot[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_10.value, index):
            """Compute the points"""
            d1 = {'x': topLeftPoint[0], 'y': y + hs}
            d2 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d1)
            valueOfLeftBottom = eval(expression, d2)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)


            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)


            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])


            d5 = {'x': x - hs, 'y': topLeftPoint[1]}
            d6 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d5)
            valueOfTopRight = eval(expression, d6)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d7 = {'x': topRightPoint[0], 'y': y + hs}
            d8 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d7)
            valueOfRightBottom = eval(expression, d8)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            """Append the Points"""
            pt3 = ([horz_zero[0], horz_zero[1]])
            pt4 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])
            all_segments .append([pt3, pt4])


        elif numpy.array_equal(IndexCases.case_11.value, index):
            """Compute the points"""
            d1 = {'x': x - hs, 'y': topLeftPoint[1]}
            d2 = {'x': x + hs, 'y': topLeftPoint[1]}
            valueOfTopLeft = eval(expression, d1)
            valueOfTopRight = eval(expression, d2)
            horz_zero = interpolateTop(topLeftPoint, topRightPoint, valueOfTopLeft, valueOfTopRight)


            d3 = {'x': topRightPoint[0], 'y': y + hs}
            d4 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d3)
            valueOfRightBottom = eval(expression, d4)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_12.value, index):
            """Compute the points"""
            d1 = {'x': topLeftPoint[0], 'y': y + hs}
            d2 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d1)
            valueOfLeftBottom = eval(expression, d2)
            vert_zero_left = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)


            d3 = {'x': topRightPoint[0], 'y': y + hs}
            d4 = {'x': topRightPoint[0], 'y': y - hs}

            valueOfRightTop = eval(expression, d3)
            valueOfRightBottom = eval(expression, d4)
            vert_zero_right = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)

            """Append the Points"""
            pt1 = ([vert_zero_right[0], vert_zero_right[1]])
            pt2 = ([vert_zero_left[0], vert_zero_left[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_13.value, index):
            """Compute the points"""
            d1 = {'x': topRightPoint[0], 'y': y + hs}
            d2 = {'x': topRightPoint[0], 'y': y - hs}
            valueOfRightTop = eval(expression, d1)
            valueOfRightBottom = eval(expression, d2)
            vert_zero = interpolateRight(topRightPoint, bottomRightPoint, valueOfRightTop, valueOfRightBottom)


            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])


        elif numpy.array_equal(IndexCases.case_14.value, index):
            """Compute the points"""
            d1 = {'x': topLeftPoint[0], 'y': y + hs}
            d2 = {'x': topLeftPoint[0], 'y': y - hs}
            valueOfLeftTop = eval(expression, d1)
            valueOfLeftBottom = eval(expression, d2)
            vert_zero = interpolateLeft(topLeftPoint, bottomLeftPoint, valueOfLeftTop, valueOfLeftBottom)


            d3 = {'x': x - hs, 'y': bottomLeftPoint[1]}
            d4 = {'x': x + hs, 'y': bottomLeftPoint[1]}
            valueOfBottomLeft = eval(expression, d3)
            valueOfBottomRight = eval(expression, d4)
            horz_zero = interpolateBottom(bottomLeftPoint, bottomRightPoint, valueOfBottomLeft, valueOfBottomRight)

            """Append the Points"""
            pt1 = ([horz_zero[0], horz_zero[1]])
            pt2 = ([vert_zero[0], vert_zero[1]])
            all_segments .append([pt1, pt2])

    """Ordering the computed line segments that form the boundary of the polygon"""
    pointsOfPolygon = []
    lastPoint = all_segments [0][0]
    referencePoint = all_segments [0][1]
    pointsOfPolygon.append(lastPoint)
    pointsOfPolygon.append(referencePoint)
    plt.plot([lastPoint[0], referencePoint[0]], [lastPoint[1], referencePoint[1]], color="Blue")
    start = True
    while referencePoint != all_segments [0][0] or start is True:
        start = False
        for seg in range(0, len(all_segments )):
            pt1 = all_segments [seg][0]
            pt2 = all_segments [seg][1]
            if pt1[0] == referencePoint[0] and pt1[1] == referencePoint[1] and \
                    pt2[0] != lastPoint[0] and pt2[1] != lastPoint[1]:
                pointsOfPolygon.append(pt2)
                lastPoint = pt1
                referencePoint = pt2
                plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color="Blue")
                break
            elif pt2[0] == referencePoint[0] and pt2[1] == referencePoint[1] and \
                pt1[0] != lastPoint[0] and pt1[1] != lastPoint[1]:
                pointsOfPolygon.append(pt1)
                lastPoint = pt2
                referencePoint = pt1
                plt.plot([pt1[0], pt2[0]], [pt1[1], pt2[1]], color="Blue")
                break

    """Segment Intersection"""
    def checkIntersection(P1, P2, P3, P4):
        x1, y1 = P1[0], P1[1]
        x2, y2 = P2[0], P2[1]
        x3, y3 = P3[0], P3[1]
        x4, y4 = P4[0], P4[1]

        if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2):
            return False
        elif max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
            return False
        else:
            segment_12_is_vertical = False
            segment_34_is_vertical = False
            #Assigning random values to prevent errors
            slope_1 = -10000
            slope_2 = -200000
            if x1 - x2 != 0:
                slope_1 = (y1 - y2) / (x1 - x2)
            else:
                segment_12_is_vertical = True
            if x3 - x4 != 0:
                slope_2 = (y3 - y4) / (x3 - x4)
            else:
                segment_34_is_vertical = False
            if  slope_1 == slope_2:
                return False
            elif (segment_12_is_vertical is True and segment_34_is_vertical is True):
                return False
            else:
                b1 = y2 - slope_1 * x2
                b2 = y4 - slope_2 * x4
                x_intersect = round(((b2 - b1) / (slope_1 - slope_2)), 3)
            if x_intersect <= max(min(x1, x2), min(x3, x4)) or x_intersect >= min(max(x1, x2), max(x3, x4)):
                return False
            else:
                return True

    """Checking for intersections"""
    hasIntersections = False
    for i in range(0, len(pointsOfPolygon) - 1):
        pt_1 = pointsOfPolygon[i]
        pt_2 = pointsOfPolygon[i + 1]
        for j in range(0, len(pointsOfPolygon) - 1):
            pt_3 = pointsOfPolygon[j]
            pt_4 = pointsOfPolygon[j + 1]
            intersect = checkIntersection(pt_1, pt_2, pt_3, pt_4)
            if intersect is True:
                hasIntersections = True
                break

    """Printable Output"""
    if len(pointsOfPolygon) - 1 == len(all_segments ) and hasIntersections is False:
        print("The constructed boundary is a simple polygon.")
    else:
        print("The constructed boundary is not a simple polygon.")

    return pointsOfPolygon



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
    plt.show()