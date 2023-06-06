import math

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, b):
        if type(b) == Vector:
            return Vector(self.x + b.x , self.y + b.y)
        return Vector(self.x + b, self.y + b)
    
    def __sub__(self, b):
        if type(b) == Vector:
            return Vector(self.x - b.x , self.y - b.y)
        return Vector(self.x - b, self.y - b)
    
    def __mul__(self, b):
        if type(b) == Vector:
            return Vector(self.x * b.x , self.y * b.y)
        return Vector(self.x * b, self.y * b)
    
    def __truediv__(self, b):
        if b == 0:
            return Vector()
        if type(b) == Vector:
            return Vector(self.x / b.x , self.y / b.y)
        return Vector(self.x / b, self.y / b)

    def GetDistance(a, b):
        dx = a.x - b.x
        dy = a.y - b.y
        return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    
    def Magnitude(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))
    
    def getTuple(self):
        return (self.x , self.y)
    
    def copy(self):
        return Vector(self.x, self.y)
    
    def __repr__(self):
        # DEBUG
        return f"vector-> ({self.x}, {self.y})"
