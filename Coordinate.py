from Polygon import Polygon

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        """
        :param another: another point which is wanted to check is the same position
        :return: True/False
        """
        return self.x == another.x and self.y == another.y

    def distance(self, point):
        return ((self.x - point.x) ** 2 + (self.y - point.y) ** 2) ** 0.5

    def Heuristic(self, goal, how = "distance"):
        """
        :param goal: goal point need to go
        :param how: function calculate Heuristic value from cur point to goal point
        :return: Heuristic value
        """
        if how == "distance":
            return self.distance(goal)

    def nearPossibleNode(self, polygons, funcCheckValid):
        """
        :param funcCheckValid: function validate point
        :param polygons: set of polygons
        :return: set of Nodes can go into
        """
        _x: Coordinate = self.x
        _y: Coordinate = self.y

        res = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    tmp = Coordinate(_x + i, _y + j)
                    if funcCheckValid(tmp):
                        res.append(tmp)

        for nearNode in res:
            for poly in polygons:
                if poly.contain_point(nearNode.x, nearNode.y):
                    res.remove(nearNode)
                    break
        return res

