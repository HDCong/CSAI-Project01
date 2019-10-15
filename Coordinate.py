
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y