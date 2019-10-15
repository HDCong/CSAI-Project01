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

"""
###################################################################
#                             BFS                                 #
###################################################################
"""


def isValidPoint(width, height, data, point):
    # check if point is out of range permission
    if point.x<0 or point.y<0 or point.y>=width or point.x>=height:
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
        if loc==end:
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

def GBFS_Algorithm(polys, start, end):
    open_set = []  # Tap chua cac dinh da mo
    visited = []   # Tap chua cac dinh da tham



"""
    Heuristic
"""


class Successor:
    def __init__(self,parrent=None,coord=None):
        self.parrent = parrent
        self.coord= coord
        ## value of a successor f = g + h
        self.g =0
        self.h =0
        self.f = 0
    def __eq__(self, another):
        return self.coord == another.coord


def findSuccessor(theList):
    successor = theList[0]
    idx =0 
    for i in range(1, len(theList)):
        if theList[i].f < successor.f:
            successor = theList[i]
            idx = i
    return successor, idx


def isDiagonal(newStep, parrent):
    if(newStep.coord.x - parrent.coord.x) * (newStep.coord.y - parrent.coord.y) != 0:
        return True
    return False


def findPathHeuristic(start,goal,data):
    width = dataRead[0][0].y
    height = dataRead[0][0].x
    # initialize open and close list
    openList = []
    closeList= []
    
    # Create base successor
    startSuccessor = Successor(None,start)

    goalSuccessor = Successor(None,goal)


    moveY = [0, 1, 1, 1, 0, -1, -1, -1]
    moveX = [1, 1, 0, -1, -1, -1, 0, 1]
    # Add start scucessor to open list
    openList.append(startSuccessor)

    while len(openList) > 0 : # not empty
        # Find successor with min-f value
        q, qIdx= findSuccessor(openList)
        # pop q off list
        openList.pop(qIdx)
        closeList.append(q)
        # if found goal 
        if q == goalSuccessor:
            path=[]
            current = q
            cost = []
            cost.append(q.g)
            while current is not None:
                path.append(current.coord)
                cost.append(current.g)
                current = current.parrent;
            return path[::-1],cost[::-1]
        
        # Generate possible successor of q
        successorList = [] 
        for i in range(8):
            possibleCoord = Coordinate(q.coord.x + moveX[i], q.coord.y + moveY[i])
            # check if the coordinate is in the grid and walkable
            if(isValidPoint(width, height,data,possibleCoord)==False):
                continue
            possibleSuccessor = Successor(q, possibleCoord)
            successorList.append(possibleSuccessor)
        
        for successor in successorList:
           for closedSuccessor in closeList:
               if successor == closedSuccessor:
                   continue

           if(isDiagonal(successor,q))==True:
               successor.g = q.g + 1.5
           else:
               successor.g = q.g + 1 
              ##  h = max { abs(current_cell.x – goal.x),abs(current_cell.y – goal.y) } 
           successor.h = ((successor.coord.x - goal.x) ** 2) + ((successor.coord.y - goal.y) ** 2)
#           delta_x= successor.coord.x - goal.x
#           delta_y=successor.coord.y - goal.y
#           successor.h = min(delta_x, delta_y) * math.sqrt(2) + abs(delta_x - delta_y)
           successor.f = successor.g + successor.h
           
           for openedSuccessor in openList:
               if successor == openedSuccessor and successor.g > openedSuccessor.g:
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

    while(not q.empty()):
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
                    if isValidPoint(width, height, data, point) and visited[newX][newY] == False and not isInPath(point, path):
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
def drawDataToGrid(data,width, heigh):
    fig, ax = plt.subplots(1, 1, tight_layout=False)

    my_cmap = colors.ListedColormap(['r', 'b', '#F7DC6F', 'g'
                                        , "#A9CCE3", "#B03A2E", "#9B59B6"
                                        , "#2980B9", "#1ABC9C", "#27AE60"
                                        , "#F39C12", "#EDBB99", "#D0ECE7"
                                        , "#EBDEF0", "#A9CCE3", "#EBDEF0", "#EBEDEF"])
    my_cmap.set_bad(color='w', alpha=0)

    bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

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


def fillPathToData(path, data, dataRead):
    color = int(len(dataRead))
    for i in range(1,len(path)-1):
        data[path[i].x][path[i].y] = color

"""
    test
"""

if __name__ == "__main__":
    
    '''bfs'''
    dataRead = read_input(wdir)
    width, heigh, data = makeDataSet(dataRead)
    path = BFS_Algorithm(width, heigh, dataRead[1][0], dataRead[1][1], data)
    # path ,cost = findPathHeuristic(dataRead[1][0], dataRead[1][1],data)
    
    fillPathToData(path, data, dataRead)
    
    drawDataToGrid(data, width, heigh)

    ''' heuristic'''
    dataRead2 = read_input(wdir)
    width, heigh, data2 = makeDataSet(dataRead2)
    # path = BFS_Algorithm(width, heigh, dataRead[1][0], dataRead[1][1],data)
    path2, cost2 = findPathHeuristic(dataRead2[1][0], dataRead2[1][1],data2)
    
    fillPathToData(path2, data2, dataRead2)
    
    drawDataToGrid(data2, width, heigh)
   
    ''' level 3'''
    dataRead3 = read_input('input2.txt')
    width3, heigh3, data3 = makeDataSet(dataRead3)

    path3 = findPathPassAllPoints(width3, heigh3, dataRead3, data3)
    
    for points in path3:
        fillPathToData(points,data3,dataRead3)
    
    drawDataToGrid(data3,width3, heigh3)
    # for i in range(len(path)):
    # print(path[i].y, path[i].x, cost[i])
