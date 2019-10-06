import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

class Coordinate:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    
wdir = 'input.txt'

"""    
    result[0][0]: size, result[0][0].x  = width, result[0][0].y = heigh
    result[1][0...n]: Coordinates of points to cross
    result[2...m][0...j]: Coordinates of vertices of a polygon
"""


def readInput(filepath): 
    result=[]
    count = 0
    with open(filepath) as fp:
       line = fp.readline()
       while line:

           line =line.replace('\n','')
           line =line.replace(' ','')
           listCoord = line.split(',')
           size = len(listCoord)
           if(size==1):
               line = fp.readline()
               continue
           result.append([])
           for x in range(0, len(listCoord)):
               if(x+1< size and x%2==0):
                   result[count].append(Coordinate(int(listCoord[x]),int(listCoord[x+1])))
           count+=1
    
           line = fp.readline()
    return result

"""
    make dataset to draw 
    
"""
def makeDataSet(dataCoord):
    width = dataRead[0][0].x
    heigh = dataRead[0][0].y
    data = np.ones((heigh, width)) * np.nan
    
    for i in range(1,len(dataCoord)):
        for j in range(len(dataCoord[i])):
            data[dataCoord[i][j].y][dataCoord[i][j].x] = i
    
    return width, heigh, data
            
###################################################################
"""
    test ket qua
"""
    
dataRead = readInput(wdir)

width, heigh, data = makeDataSet(dataRead)


fig, ax = plt.subplots(1, 1, tight_layout=False)

my_cmap = colors.ListedColormap(['r', 'b', 'y', 'g', 'c'])

my_cmap.set_bad(color='w', alpha=0)

bounds= [0,1,2,3,4,5,6]

norm = colors.BoundaryNorm(bounds, my_cmap.N)

# draw the grid
for x in range(heigh +1):
    ax.axhline(x, lw=1, color='k')
    
for x in range(width+1):
    ax.axvline(x, lw=1, color='k')
    

ax.set_xticks(np.arange(0, width+1, 1));
ax.set_yticks(np.arange(0, heigh+1, 1));
ax.grid(which='both')


ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, 22, 0, 18],origin='lower',norm = norm)


plt.gcf().set_size_inches((10, 10))    
plt.show()