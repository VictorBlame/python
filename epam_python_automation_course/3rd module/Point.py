class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'X: ' + str(self.x) + ', Y:' + str(self.y)


class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z

    def __str__(self):
        return super().__str__() + ', Z: ' + str(self.z)


point1 = Point(1, 6)
point2 = Point(-7, 21)
point3 = Point3D(6, 8, -3)
print(point1.__str__())
print(point2.__str__())
print(point3.__str__())

