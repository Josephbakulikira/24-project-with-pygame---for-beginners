from math import sqrt, pow

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __add__(self, b):
        if type(b) == Vector2:
            return Vector2(self.x + b.x, self.y + b.y)
        return Vector2(self.x + b, self.y + b)
    
    def __sub__(self, b):
        if type(b) == Vector2:
            return Vector2(self.x - b.x, self.y - b.y)
        return Vector2(self.x - b, self.y - b)
    
    def __mul__(self, b):
        if type(b) == Vector2:
            return Vector2(self.x * b.x , self.y * b.y)
        return Vector2(self.x * b, self.y * b)
    
    def __truediv__(self, b):
        if type(b) == Vector2:
            return Vector2(self.x / b.x, self.y / self.y)
        return Vector2(self.x / b, self.y / b)
    
    def magnitude(self):
        return sqrt(pow(self.x, 2) + pow(self.y, 2))
    
    def setMagnitude(self, new_magnitude):
        return Normalize(self) * new_magnitude
    
    def ParseToInt(self):
        return (int(self.x), int(self.y))

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

def GetMagnitude(a):
    return sqrt(pow(a.x, 2) + pow(a.y, 2))

def Normalize(a):
    mg = GetMagnitude(a)
    if mg == 0:
        return Vector2()
    return Vector2(a.x/mg, a.y/mg)

def SetMagnitude(vec, mag):
    normalizedVec = Normalize(vec)
    return normalizedVec * mag

def GetDistance2D(a, b):
    difference = b - a
    return difference.magnitude()