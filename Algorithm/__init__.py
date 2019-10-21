import numpy as np

"""
    Helper function for Algorithm
"""


def isValidPoint(width, height, data, point):
    # check if point is out of range permission
    if point.x < 0 or point.y < 0 or point.y >= width or point.x >= height:
        return False
    # check if destination
    if data[point.x][point.y] == 1:
        return True
    # check if point is object
    if not np.isnan(data[point.x][point.y]):
        return False
    # default
    return True


def getPath(start, loc, parent):
    path = []
    backtrack = loc
    while backtrack != start:
        path.append(backtrack)
        backtrack = parent[backtrack.x][backtrack.y]
    path.append(start)
    path.reverse()
    return path
