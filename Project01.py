from Graphic import *
from Animation import *
from Polygon import Polygon
from matplotlib import colors
from Coordinate import Coordinate

import queue
import functools
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
wdir = 'input.txt'

# Global variable

# Define Colors to paint
my_cmap = colors.ListedColormap(
    ["r", "b", '#F7DC6F', "g", "#A9CCE3",
     "#B03A2E", "#9B59B6", "#2980B9", "#1ABC9C", "#27AE60",
     "#F39C12", "#EDBB99", "#D0ECE7", "#EBDEF0", "#A9CCE3", "#EBDEF0", "#EBEDEF"
     ])
bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
norm = colors.BoundaryNorm(bounds, my_cmap.N)

# Configure
my_cmap.set_bad(color='w', alpha=0)

"""    
    result[0][0]: size, result[0][0].y  = width, result[0][0].x = heigh
    result[1][0...n]: Coordinates of points to cross
    result[2...m][0...j]: Coordinates of vertices of a polygon
"""


def read_input(filepath):
    result = []
    count = 0
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line = line.replace('\n', '')
            line = line.replace(' ', '')
            list_coord = line.split(',')
            size = len(list_coord)
            if size == 1:
                line = fp.readline()
                continue
            result.append(Polygon())
            for x in range(0, len(list_coord)):
                if x + 1 < size and x % 2 == 0:
                    result[count].append_point(Coordinate(int(list_coord[x + 1]), int(list_coord[x])))
            count += 1
            line = fp.readline()
    return result


"""
    make dataset to draw 
"""


def makeDataSet(dataCoord):
    width = dataCoord[0][0].y
    height = dataCoord[0][0].x
    data = np.ones((height, width)) * np.nan

    for i in range(1, len(dataCoord)):
        size = dataCoord[i].size if isinstance(dataCoord[i], Polygon) else len(dataCoord[i])
        for j in range(size):
            data[dataCoord[i][j].x][dataCoord[i][j].y] = int(i)
        if i > 1:
            min_x, min_y, max_x, max_y = dataCoord[i].find_rectangle()
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if dataCoord[i].contain_point(x, y):
                        data[x][y] = i
            for j in range(size - 1):
                plotLine(data, dataCoord[i][j], dataCoord[i][j + 1], i)
            plotLine(data, dataCoord[i][size - 1], dataCoord[i][0], i)
    return width, height, data


"""
    Algorithms
"""

"""
###################################################################
#                             BFS                                 #
###################################################################
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


"""
    Greedy Best First Search
"""


def GBFS_Algorithm(polys, start: Coordinate, end: Coordinate, width: int, height: int, data):
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
    return None


def GBFS_Algorithm_with_Animation(polys, start: Coordinate, end: Coordinate, width: int, height: int, data):
    open_set = []
    for u in start.nearPossibleNode(polys, functools.partial(isValidPoint, width, height, data)):
        u.h = u.Heuristic(end)
        open_set.append(u)
    v = min(open_set, key=lambda x: x.h)  # Su dung thuat toan tham lam lay diem cok heuristic nho nhat
    return v


"""
    A* 
"""


class Successor:
    def __init__(self, parrent=None, coord=None):
        self.parrent = parrent
        self.coord = coord

        # Value of a successor f = g + h
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, another):
        return self.coord == another.coord


def findSuccessor(theList):
    successor = theList[0]
    idx = 0
    for i in range(1, len(theList)):
        if theList[i].f < successor.f:
            successor = theList[i]
            idx = i
    return successor, idx


def isDiagonal(newStep, parrent):
    if (newStep.coord.x - parrent.coord.x) * (newStep.coord.y - parrent.coord.y) != 0:
        return True
    return False


def findPathHeuristic(start, goal, data, width, height):
    # initialize open and close list
    openList = []
    closeList = []

    # Create base successor
    startSuccessor = Successor(None, start)

    goalSuccessor = Successor(None, goal)

    moveY = [0, 0, 1, -1, 1, -1, -1, 1]
    moveX = [1, -1, 0, 0, -1, -1, 1, 1]
    # Add start scucessor to open list
    openList.append(startSuccessor)

    while len(openList) > 0:  # not empty
        # Find successor with min-f value
        q, qIdx = findSuccessor(openList)
        # pop q off list
        openList.pop(qIdx)
        closeList.append(q)
        # if found goal 
        if q == goalSuccessor:
            path = []
            current = q
            cost = [q.g]
            while current is not None:
                path.append(current.coord)
                cost.append(current.g)
                current = current.parrent
            return path[::-1], cost

        # Generate possible successor of q
        successorList = []
        for i in range(8):
            possibleCoord = Coordinate(q.coord.x + moveX[i], q.coord.y + moveY[i])
            # check if the coordinate is in the grid and walkable
            if not isValidPoint(width, height, data, possibleCoord):
                continue
            # if possilbe , create new successor with its coord
            possibleSuccessor = Successor(q, possibleCoord)

            successorList.append(possibleSuccessor)

        # check if in the close list
        for successor in successorList:
            for closedSuccessor in closeList:
                if successor == closedSuccessor and successor.f > closedSuccessor.f:
                    continue
            # value of diagonal is 1.5
            if isDiagonal(successor, q):
                successor.g = q.g + 1.5
            else:
                successor.g = q.g + 1

                # heuristic is: (x-xG)^2 + ( y-yG)^2
            successor.h = (successor.coord.x - goal.x) ** 2 + (successor.coord.y - goal.y) ** 2
            # f= g + h
            successor.f = successor.g + successor.h
            # check if it in the openlist and openlist has f value < its f value
            for openedSuccessor in openList:
                if successor == openedSuccessor and successor.f > openedSuccessor.f:
                    continue
            openList.append(successor)


""" 
    Level 3
"""


###################################################################
#      Find route from Start to End visits all given points       #
###################################################################

def getPoints(dataRead):
    points = []
    for i in range(2, len(dataRead[1].points)):
        points.append(dataRead[1][i])
    return points


def getSubPath(start, loc, parent):
    path = []
    backtrack = loc
    while backtrack != start:
        path.append(backtrack)
        backtrack = parent[backtrack.x][backtrack.y]

    path.append(start)
    path.reverse()
    return path


def isInPath(point, Path):
    for path in Path:
        for p in path:
            if point.x == p.x and point.y == p.y:
                return True
    return False


def clearQueue(queue):
    while not queue.empty():
        queue.get()


def removePoint(point, l):
    for p in l:
        if p.x == point.x and p.y == point.y:
            l.remove(p)


def isPointInSet(point, s):
    for p in s:
        if point.x == p.x and point.y == p.y:
            return True
    return False


def findPath(width, height, start, end, data, points):
    path = []

    begin = start

    visited = [[False for y in range(width)] for x in range(height)]
    # list of parents
    parent = [[start for y in range(width)] for x in range(height)]

    # cho phep di cheo 
    y = [0, 1, 1, 1, 0, -1, -1, -1]
    x = [1, 1, 0, -1, -1, -1, 0, 1]

    # khong cho phep di cheo
    # y = [0, 1, 0, -1]
    # x = [1, 0, -1, 0]

    lenLoop = len(y)

    q = queue.Queue(maxsize=0)
    q.put(start)
    visited[start.x][start.y] = True

    while not q.empty():
        loc = q.get()

        if isPointInSet(loc, points):
            path.append(getSubPath(begin, loc, parent))
            begin = loc
            removePoint(loc, points)
            clearQueue(q)
            q.put(loc)
            visited = [[False for y in range(width)] for x in range(height)]
        else:
            if loc.x == end.x and loc.y == end.y and len(points) == 0:
                path.append(getSubPath(begin, loc, parent))
                break
            else:
                for i in range(lenLoop):
                    newX = loc.x + x[i]
                    newY = loc.y + y[i]
                    point = Coordinate(int(newX), int(newY))
                    if not isValidPoint(width, height, data, point) \
                            and visited[newX][newY] \
                            and not isInPath(point, path):
                        q.put(point)
                        parent[newX][newY] = loc
                        visited[newX][newY] = True

    return path


def findPathPassAllPoints(width, height, dataRead, dataset):
    points = getPoints(dataRead)

    start = dataRead[1][0]
    end = dataRead[1][1]

    path = findPath(width, height, start, end, dataset, points)

    return path


# essential functions
def drawDataToGrid(data, width, height, title: str):
    global my_cmap, bounds, norm
    fig, ax = plt.subplots(1, 1, tight_layout=False)
    fig.suptitle(title, fontsize=16)
    drawGrid(ax, height, width)
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, width, 0, height], origin='lower', norm=norm)
    plt.gcf().set_size_inches((10, 10))
    plt.show()


def drawGrid(ax, height, width):
    # draw the grid
    for x in range(height + 1):
        ax.axhline(x, lw=1, color='k')
    for x in range(width + 1):
        ax.axvline(x, lw=1, color='k')
    ax.set_xticks(np.arange(0, width + 1, 1))
    ax.set_yticks(np.arange(0, height + 1, 1))
    ax.grid(which='both')


def fillPathToData(path, data, dataRead):
    color = int(len(dataRead))
    for i in range(1, len(path) - 1):
        data[path[i].x][path[i].y] = color


if __name__ == "__main__":

    #      Level 1 & 2
    ''' BFS'''
    dataRead1 = read_input(wdir)
    width1, heigh1, data1 = makeDataSet(dataRead1)
    path1 = BFS_Algorithm(width1, heigh1, dataRead1[1][0], dataRead1[1][1], data1)
    fillPathToData(path1, data1, dataRead1)
    drawDataToGrid(data1, width1, heigh1, 'BFS')

    ''' gbfs'''
    dataRead5 = read_input(wdir)
    width5, heigh5, data5 = makeDataSet(dataRead5)
    start5 = Coordinate(dataRead5[1][0].x, dataRead5[1][0].y)
    end5 = Coordinate(dataRead5[1][1].x, dataRead5[1][1].y)
    path5 = GBFS_Algorithm(dataRead5[2:], start5, end5, width5, heigh5, data5)
    fillPathToData(path5, data5, dataRead5)
    drawDataToGrid(data5, width5, heigh5, 'GBFS')

    ''' A* '''
    dataRead2 = read_input(wdir)

    width2, heigh2, data2 = makeDataSet(dataRead2)

    path2, cost2 = findPathHeuristic(dataRead2[1][0], dataRead2[1][1], data2, width2, heigh2)

    fillPathToData(path2, data2, dataRead2)
    drawDataToGrid(data2, width2, heigh2, 'A*')

    # Level 3

    ''' multi point'''
    dataRead3 = read_input('input2.txt')
    width3, heigh3, data3 = makeDataSet(dataRead3)

    path3 = findPathPassAllPoints(width3, heigh3, dataRead3, data3)

    for points in path3:
        fillPathToData(points, data3, dataRead3)

    drawDataToGrid(data3, width3, heigh3, 'Multi points')

    ''' animation '''

    dataRead4 = read_input(wdir)
    width4, height4, data4 = makeDataSet(dataRead4)

    fig4, ax4 = plt.subplots(1, 1, tight_layout=True)
    fig4.suptitle('Animation', fontsize=10)

    start4 = Coordinate(dataRead4[1][0].x, dataRead4[1][0].y)
    end4 = Coordinate(dataRead4[1][1].x, dataRead4[1][1].y)

    drawGrid(ax4, height4, width4)

    plt.ion()
    next_node4 = start4
    while not next_node4 == end4:
        movePolygons(dataRead4, data4, width4, height4)

        data4[next_node4.x][next_node4.y] = np.nan
        next_node4 = GBFS_Algorithm_with_Animation(dataRead4[2:], next_node4, end4, width4, height4, data4)
        data4[next_node4.x][next_node4.y] = 1

        drawGrid(ax4, height4, width4)

        ax4.imshow(data4, interpolation='none', cmap=my_cmap, extent=[0, width4, 0, height4], origin='lower', norm=norm)
        plt.pause(0.1)
        plt.cla()
