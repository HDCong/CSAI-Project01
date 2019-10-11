import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from Coordinate import Coordinate
from Polygon import Polygon
import queue
import math

wdir = 'input.txt'

"""    
    result[0][0]: size, result[0][0].x  = width, result[0][0].y = heigh
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
    width = dataRead[0][0].y
    heigh = dataRead[0][0].x
    data = np.ones((heigh, width)) * np.nan

    for i in range(1, len(dataCoord)):
        size = dataCoord[i].size if isinstance(dataCoord[i], Polygon) else len(dataCoord[i].size)
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
    return width, heigh, data


"""
    Draw a line: 
    Source: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm?fbclid=IwAR0TiBG42hKE7Xi3IfoWshVTgltjWdE8utajs4fWc_sGcrZWrj7nO09uQtY
"""


def plotLine(data, fromCoord, toCoord, index):
    x0, y0 = fromCoord.x, fromCoord.y
    x1, y1 = toCoord.x, toCoord.y

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(data, toCoord, fromCoord, index)
        else:
            plotLineLow(data, fromCoord, toCoord, index)
    else:
        if y0 > y1:
            plotLineHigh(data, toCoord, fromCoord, index)
        else:
            plotLineHigh(data, fromCoord, toCoord, index)


def plotLineLow(data, fromCoord, toCoord, index):
    x0, y0 = fromCoord.x, fromCoord.y
    x1, y1 = toCoord.x, toCoord.y
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = 2 * dy - dx
    y = y0

    for x in range(x0, x1):
        data[x][y] = index
        if D > 0:
            y = y + yi
            D = D - 2 * dx
        D = D + 2 * dy


def plotLineHigh(data, fromCoord, toCoord, index):
    x0, y0 = fromCoord.x, fromCoord.y
    x1, y1 = toCoord.x, toCoord.y
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2 * dx - dy
    x = x0

    for y in range(y0, y1):
        data[x][y] = index
        if D > 0:
            x = x + xi
            D = D - 2 * dx
        D = D + 2 * dx

#######################################################################

"""
    Algorithms
"""


# BFS 
###################################################################

def isValidPoint(width, height, data, point):
  # check if point is out of range permission
    if point.x<1 or point.y<1 or point.y>=width or point.x>=height:
        return False 
  # check if destination
    if data[point.x][point.y] == 1:
        return True
  # check if point is object
    if not math.isnan(data[point.x][point.y]):
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

    y = [0, 1, 1, 1, 0, -1, -1, -1]
    x = [1, 1, 0, -1, -1, -1, 0, 1]

    q = queue.Queue(maxsize=0)
    q.put(start)
    visited[start.x][start.y] = True

  # implement
    while(not q.empty()):
        loc = q.get()
        if loc.x == end.x and loc.y == end.y:
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


def draw(width, heigh, data):
    fig, ax = plt.subplots(1, 1, tight_layout=False)

    my_cmap = colors.ListedColormap(["red", "orange", "gold", "limegreen", "k","#550011", "purple", "seagreen"])

    my_cmap.set_bad(color='w', alpha=0)

    bounds = [0, 1, 2, 3, 4, 5, 6,7,8,9,10]

    norm = colors.BoundaryNorm(bounds, my_cmap.N)

    # draw the grid
    for x in range(heigh + 1):
        ax.axhline(x, lw=1, color='k')

    for x in range(width + 1):
        ax.axvline(x, lw=1, color='k')

    ax.set_xticks(np.arange(0, width + 1, 1))
    ax.set_yticks(np.arange(0, heigh + 1, 1))
    ax.grid(which='both')

    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, width, 0, heigh], origin='lower', norm=norm)

    plt.gcf().set_size_inches((10, 10))
    plt.show()
def fillPathToGrid(data, path, dataInput):
    color = int(len(dataInput)+1)
    for i in range(1,len(path)-1):
        data[list[i].x][list[i].y]= color
        
"""
    test ket qua
"""       
if __name__ == "__main__":
    dataRead = read_input(wdir)
    width, heigh, dataSet = makeDataSet(dataRead)
    
    list = BFS_Algorithm(width, heigh, dataRead[1][0], dataRead[1][1], dataSet)

    fillPathToGrid(dataSet,list,dataRead)

    draw(width, heigh, dataSet)
