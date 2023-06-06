import math
import random

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, b):
        if type(b) == Vector:
            return Vector(self.x + b.x, self.y + b.y)
        return Vector(self.x + b, self.y + b)
    
    def __sub__(self, b):
        if type(b) == Vector:
            return Vector(self.x - b.x, self.y - b.y)
        return Vector(self.x - b, self.y - b)
    
    def __truediv__(self, b):
        if type(b) == Vector:
            return Vector(self.x / b.x, self.y / b.y)
        return Vector(self.x / b, self.y / b)

    def __mul__(self, b):
        if type(b) == Vector:
            return Vector(self.x * b.x, self.y * b.y)
        return Vector(self.x * b, self.y * b)
    
    def GetDistance(a, b):
        dx2 = (a.x - b.x) ** 2
        dy2 = (a.y - b.y) ** 2
        return math.sqrt(dx2+dy2)
    
    def fromAngle(angle, scale=1):
        return Vector(math.sin(angle) * scale, -math.cos(angle) * scale)

    def magnitude(self):
        a = self.x ** 2
        b = self.y ** 2
        return math.sqrt(a+b)
    
    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return self/mag
        return Vector(0, 0)
    
    def getTuple(self):
        return (int(self.x), int(self.y))
    
    def SetMagnitude(vec, new_mag):
        v = vec.normalize()
        return v * new_mag
    
    def Limit(vec, max_mag):
        mag = vec.magnitude()
        if mag > max_mag:
            return Vector.SetMagnitude(vec, max_mag)
        return vec
    
    def Heading(vec):
        angle = math.atan2(vec.y, vec.x)
        # degrees = 180 * angle / math.pi
        #return angle in radians
        return angle

    
    def Random(min_val, max_val):
        choices = [-1, 1]
        value = random.randint(min_val, max_val)
        x = random.choice(choices) * value
        y = random.choice(choices) * value
        return Vector(x, y)
    
    def __repr__(self):
        # DEBUG
        return f"x: {self.x}, y: {self.y}"