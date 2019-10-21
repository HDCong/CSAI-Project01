import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt

# Define Colors to paint
my_cmap = colors.ListedColormap(
    ["r", "b", '#F7DC6F', "g", "#A9CCE3",
     "#B03A2E", "#9B59B6", "#2980B9", "#1ABC9C",
     "#27AE60", "#F39C12", "#EDBB99", "#D0ECE7",
     "#EBDEF0", "#A9CCE3", "#EBDEF0", "#EBEDEF"
     ])
bounds = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
norm = colors.BoundaryNorm(bounds, my_cmap.N)

# Configure
my_cmap.set_bad(color='w', alpha=0)

"""
    Draw a line:
    Source:
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm?fbclid=IwAR0TiBG42hKE7Xi3IfoWshVTgltjWdE8utajs4fWc_sGcrZWrj7nO09uQtY
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
