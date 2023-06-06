import math
import colorsys

def euclideanDistance(a, b):
    dist = (a.x - b.x )*(a.x - b.x ) + (a.y - b.y)*(a.y - b.y)
    return math.sqrt(dist)

def AreDiagonal(a, b, diagonalCheck=False):
    #bottom-right
    if a.x + 1 == b.x and a.y+1 == b.y:

        return True
    #top-right
    elif a.x + 1 == b.x and a.y-1 == b.y:
        return True
    #bottom-left
    elif a.x - 1 == b.x and a.y + 1 == b.y:
        return True
    #top-left
    elif a.x - 1 == b.x and a.y - 1 == b.y:
        return True
    else:
        return False