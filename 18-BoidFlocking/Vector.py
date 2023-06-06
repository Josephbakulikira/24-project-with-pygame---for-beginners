import math

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
    
    def __mul__(self, b):
        if type(b) == Vector:
            return Vector(self.x * b.x, self.y * b.y)
        return Vector(self.x * b, self.y * b)
    
    def __truediv__(self, b):
        if type(b) == Vector:
            return Vector(self.x / b.x, self.y / b.y)
        return Vector(self.x / b, self.y / b)
    
    def fromAngle(angle, scale=1):
        x = math.cos(angle) * scale
        y = math.sin(angle) * scale
        return Vector(x, y)
    
    def Heading(vec):
        angle = math.atan2(vec.y, vec.x)
        # degrees = 180 * angle / math.pi
        #return angle in radians
        return angle

    def Magnitude(vec):
        return math.sqrt(vec.x ** 2 + vec.y ** 2)

    def Normalize(vec):
        magnitude = Vector.Magnitude(vec)
        return vec/magnitude
    
    def SetMagnitude(vec, new_mag):
        normalized = Vector.Normalize(vec)
        return normalized * new_mag
    
    def GetTuple(self):
        return (self.x, self.y)
    
    def Limit(self, value):
        magnitude = Vector.Magnitude(self)
        if abs(magnitude) > value:
            return Vector.SetMagnitude(self, value)
        else:
            return Vector(self.x, self.y)
        
    
    def __repr__(self):
        #DEBUG
        return f"({self.x}, {self.y})"

def Distance(a, b):
    f = math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)
    return math.sqrt(f)