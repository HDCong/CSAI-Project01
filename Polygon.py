class Polygon:
    def __init__(self):
        self.size = 0
        self.points = []

    def get_points(self):
        return self.points

    def append_point(self, point):
        self.size += 1
        self.points.append(point)

    def __getitem__(self, item):
        return self.points[item]
    
    def moveLeft(self):
        for point in self.points:
            point.updateCoord(-1, 0)
    def moveRight(self):
        for point in self.points:
            point.updateCoord(1, 0)    
    def moveUp(self):
        for point in self.points:
            point.updateCoord(0, 1)
    def moveDown(self):
        for point in self.points:
            point.updateCoord(0, -1)
    """
        Decide a given coordinate is inside a polygon
        Source: http://www.ariel.com.au/a/python-point-int-poly.html
    """

    def contain_point(self, x, y):
        n = self.size
        inside = False

        p1x, p1y = self.points[0].x, self.points[0].y
        for i in range(n + 1):
            p2x, p2y = self.points[i % n].x, self.points[i % n].y
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / float((p2y - p1y)) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    """
        find the bottom-left point and top-right point    
    """

    def find_rectangle(self):
        list_x = []
        list_y = []
        for i in range(self.size):
            list_x.append(self.points[i].x)
            list_y.append(self.points[i].y)
        return min(list_x), min(list_y), max(list_x), max(list_y)

