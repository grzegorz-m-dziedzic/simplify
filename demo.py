from simplify import simplify


@simplify
class Point3D:
    def __init__(self, x, y, z): pass

    def distance(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


p1 = Point3D(1, 2, 3)
p2 = Point3D(1, 2, 3)
p3 = Point3D(2, 3, 5)

print(p1 == p2)
print(p2 == p3)

print(p1)
print(p2)

print(p1.distance(p3))

l = [p3, p1]
print(l)
l.sort()
print(l)
