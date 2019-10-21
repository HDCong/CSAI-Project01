from Algorithm import isValidPoint
from Coordinate import Coordinate

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

    moveX = [0, 1, 1, 1, 0, -1, -1, -1]
    moveY = [1, 1, 0, -1, -1, -1, 0, 1]
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
                if successor == closedSuccessor and successor.g > closedSuccessor.g:
                    continue
            # check if it in the openlist and openlist has g value < its g value
            for openedSuccessor in openList:
                if successor == openedSuccessor and successor.g > openedSuccessor.g:
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
            openList.append(successor)
        if len(openList) > width * height * 8:
            # can not find
            return [], []
