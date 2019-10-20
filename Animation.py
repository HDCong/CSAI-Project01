import math
import random
import numpy as np

"""
  Level 4: Animation
"""


def isNotConflict(min_x, min_y, max_x, max_y, data, width, height, idx):
    if min_x < 0 or min_y < 0 or max_x >= height or max_y >= width:
        return False
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if not np.isnan(data[i][j]):
                if int(data[i][j]) != idx:
                    return False
    return True


def updateMat(data, Polygon, action, idx):
    min_x, min_y, max_x, max_y = Polygon.find_rectangle()

    if action == 0:  # left
        for i in range(min_x - 1, max_x):
            for j in range(min_y, max_y + 1):
                if not math.isnan(data[i + 1][j]):
                    if data[i + 1][j] == idx:
                        data[i][j] = data[i + 1][j]
                    else:
                        data[i][j] = math.nan
                else:
                    data[i][j] = math.nan
        for j in range(min_y, max_y + 1):
            if not math.isnan(data[max_x][j]):
                if data[max_x][j] == idx:
                    data[max_x][j] = math.nan
    elif action == 1:  # right
        for i in range(max_x + 1, min_x, -1):
            for j in range(min_y, max_y + 1):
                if not math.isnan(data[i - 1][j]):
                    if data[i - 1][j] == idx:
                        data[i][j] = data[i - 1][j]
                    else:
                        data[i][j] = math.nan
                else:
                    data[i][j] = math.nan
        for j in range(min_y, max_y + 1):
            if not math.isnan(data[min_x][j]):
                if data[min_x][j] == idx:
                    data[min_x][j] = math.nan
    elif action == 2:  # down
        for i in range(min_y - 1, max_y):
            for j in range(min_x, max_x + 1):
                if not math.isnan(data[j][i + 1]):
                    if data[j][i + 1] == idx:
                        data[j][i] = data[j][i + 1]
                    else:
                        data[j][i] = math.nan
                else:
                    data[j][i] = math.nan
        for j in range(min_x, max_x + 1):
            if not math.isnan(data[j][max_y]):
                if data[j][max_y] == idx:
                    data[j][max_y] = np.nan
    else:  # up
        for i in range(max_y + 1, min_y, -1):
            for j in range(min_x, max_x + 1):
                if not math.isnan(data[j][i - 1]):
                    if data[j][i - 1] == idx:
                        data[j][i] = data[j][i - 1]
                    else:
                        data[j][i] = math.nan
                else:
                    data[j][i] = math.nan
        for j in range(min_x, max_x + 1):
            if not math.isnan(data[j][min_y]):
                if data[j][min_y] == idx:
                    data[j][min_y] = math.nan


#    return data


def movePolygons(dataRead, data, width, heigh):
    #    print("vao move poly")
    for i in range(2, len(dataRead)):
        min_x, min_y, max_x, max_y = dataRead[i].find_rectangle()
        number = random.randint(0, 4)  # random direction
        #        print(i,":",min_x, min_y, max_x, max_y)
        if isNotConflict(min_x - 1, min_y, max_x - 1, max_y, data, width, heigh, i) == True and number == 0:
            #            print("1")
            updateMat(data, dataRead[i], 0, i)
            dataRead[i].moveLeft()
        elif isNotConflict(min_x, min_y + 1, max_x, max_y + 1, data, width, heigh, i) == True and number == 1:
            #            print("2")
            updateMat(data, dataRead[i], 3, i)
            dataRead[i].moveUp()
        elif isNotConflict(min_x + 1, min_y, max_x + 1, max_y, data, width, heigh, i) == True and number == 2:
            #            print("3")
            updateMat(data, dataRead[i], 1, i)
            dataRead[i].moveRight()
        elif isNotConflict(min_x, min_y - 1, max_x, max_y - 1, data, width, heigh, i) == True and number == 3:
            #            print("5")
            updateMat(data, dataRead[i], 2, i)
            dataRead[i].moveDown()
    return data