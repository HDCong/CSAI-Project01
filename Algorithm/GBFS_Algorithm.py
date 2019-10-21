import functools
from Coordinate import Coordinate
from Algorithm import isValidPoint

"""
###################################################################
#                 GBFS - Greedy Best First Search                 #
###################################################################
"""


def GBFS_Algorithm(polys, start: Coordinate, end: Coordinate, width: int, height: int, data):
    """
    :param polys: List of input polygons
    :param start: start point
    :param end: goal point
    :param width: width of map
    :param height: height of map
    :param data: 2D array representation of map
    :return: path from start to goal
    """
    open_set = []  # Tap chua cac dinh da mo
    visited = []  # Tap chua cac dinh da tham
    start.parentNode = None
    start.h = start.Heuristic(end)
    open_set.append(start)

    while open_set:
        v = min(open_set, key=lambda x: x.h)  # Su dung thuat toan tham lam lay diem cok heuristic nho nhat
        if v == end:
            path = []
            while v:
                path.append(v)
                v = v.parentNode
            return path[::-1]

        open_set.remove(v)
        visited.append(v)

        u: Coordinate = None
        for u in v.nearPossibleNode(polys, functools.partial(isValidPoint, width, height, data)):
            if u in visited:
                continue

            if u not in open_set:
                u.h = u.Heuristic(end)
                u.parentNode = v
                open_set.append(u)
    return []


def GBFS_Algorithm_with_Animation(polys, start: Coordinate, end: Coordinate, width: int, height: int, data):
    open_set = []
    for u in start.nearPossibleNode(polys, functools.partial(isValidPoint, width, height, data)):
        u.h = u.Heuristic(end)
        open_set.append(u)
    v = min(open_set, key=lambda x: x.h)  # Su dung thuat toan tham lam lay diem cok heuristic nho nhat
    return v
