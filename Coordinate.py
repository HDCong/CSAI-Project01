
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, another):
        return self.x == another.x and self.y == another.y
    
    def updateCoord(self,delta_x,delta_y):
        self.x = self.x + delta_x
        self.y = self.y + delta_y