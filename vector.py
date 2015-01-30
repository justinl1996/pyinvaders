__author__ = 'justin'
import math

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, other):
        self.x *= other
        self.x *= other

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self.x, self.y

    def get_angle(self):
        return round(math.degrees(math.atan(self.y/self.x)), 2)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def __repr__(self):
        return "Vector({0},{1})".format(self.x, self.y)


a = Vector(1, 3)
b = Vector(4, 6)
#print a.get_angle()
#print b.get_angle()

