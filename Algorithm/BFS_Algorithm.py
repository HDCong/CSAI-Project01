from Algorithm import *

import queue
from Coordinate import Coordinate

"""
###################################################################
#                             BFS                                 #
###################################################################
"""


def BFS_Algorithm(width, height, start, end, data):
    # init
    # shortest path result
    result = []
    # list of visited points
    visited = [[False for y in range(width)] for x in range(height)]
    # list of parents
    parent = [[start for y in range(width)] for x in range(height)]

    y = [0, -1, 1, 0, 1, -1, 1, -1]
    x = [1, 0, 0, -1, -1, -1, 1, 1]

    q = queue.Queue(maxsize=0)
    q.put(start)
    visited[start.x][start.y] = True

    # implement
    while not q.empty():
        loc = q.get()
        if loc == end:
            result = getPath(start, loc, parent)
            break
        else:
            for i in range(8):
                newX = loc.x + x[i]
                newY = loc.y + y[i]
                point = Coordinate(int(newX), int(newY))
                if isValidPoint(width, height, data, point) and visited[newX][newY] == False:
                    q.put(point)
                    parent[newX][newY] = loc
                    visited[newX][newY] = True

    return result
