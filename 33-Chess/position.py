from constants import *

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if other == None:
            return False
        elif self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    
    def Compare(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False
    
    def GetCopy(self):
        return Position(self.x, self.y)
    
    def getTuple(self):
        return (self.x, self.y)
    
    def OnBoard(self):
        # Checking if the position is not out of the playing board
        if (self.x >= 0 and self.x < 8) and (self.y >= 0 and self.y < 8):
            return True
        return False
        
    
    def __repr__(self):
        # DEBUG
        return f"({self.x}, {self.y})"