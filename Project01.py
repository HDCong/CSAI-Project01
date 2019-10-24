from Animation import *
from Graphic import *
from Polygon import Polygon
from Coordinate import Coordinate
from Algorithm import BFS_Algorithm
from Algorithm import GBFS_Algorithm
from Algorithm import AStar_Algorithm

import queue
import functools
import Algorithm
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
wdir = "./Input/input4.txt" # input("Nhập vào đường dẫn file đầu vào: ")


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
                    if Algorithm.isValidPoint(width, height, data, point) and visited[newX][newY] == False and not isInPath(point, path):
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


if __name__ == "__main__":

    # Level 1 & 2
    ''' BFS'''
    dataRead1 = read_input(wdir)
    width1, heigh1, data1 = makeDataSet(dataRead1)
    path1 = BFS_Algorithm.BFS_Algorithm(width1, heigh1, dataRead1[1][0], dataRead1[1][1], data1)
    fillPathToData(path1, data1, dataRead1)
    drawDataToGrid(data1, width1, heigh1, 'BFS')

    ''' gbfs'''
    dataRead5 = read_input(wdir)
    width5, heigh5, data5 = makeDataSet(dataRead5)
    start5 = Coordinate(dataRead5[1][0].x, dataRead5[1][0].y)
    end5 = Coordinate(dataRead5[1][1].x, dataRead5[1][1].y)
    path5 = GBFS_Algorithm.GBFS_Algorithm(dataRead5[2:], start5, end5, width5, heigh5, data5)
    fillPathToData(path5, data5, dataRead5)
    drawDataToGrid(data5, width5, heigh5, 'GBFS')

    ''' A* '''
    dataRead2 = read_input(wdir)

    width2, heigh2, data2 = makeDataSet(dataRead2)

    path2, cost2 = AStar_Algorithm.findPathHeuristic(dataRead2[1][0], dataRead2[1][1], data2, width2, heigh2)

    fillPathToData(path2, data2, dataRead2)
    drawDataToGrid(data2, width2, heigh2, 'A*')

    # Level 3

    ''' multi point'''
    dataRead3 = read_input('./Input/input4.txt')
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
        next_node4 = GBFS_Algorithm.GBFS_Algorithm_with_Animation(dataRead4[2:], next_node4, end4, width4, height4, data4)
        data4[next_node4.x][next_node4.y] = 1

        drawGrid(ax4, height4, width4)

        ax4.imshow(data4, interpolation='none', cmap=my_cmap, extent=[0, width4, 0, height4], origin='lower', norm=norm)
        plt.pause(0.2)
        plt.cla()
