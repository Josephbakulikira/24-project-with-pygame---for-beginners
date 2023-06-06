import math
from constants import *
from vector import Vector

def LineLineIntersection(pointA, pointB, pointC, pointD):
    # LINE 1 (PointA, pointB)
    x1 = pointA.x
    y1 = pointA.y
    x2 = pointB.x
    y2 = pointB.y
    # LINE 2 (PointC, pointC)
    x3 = pointC.x
    y3 = pointC.y
    x4 = pointD.x
    y4 = pointD.y

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denominator == 0:
        # Return None if the two lines are paralleles
        return None
    # Calculate t
    T_numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    t = T_numerator / denominator

    # calculate  u
    U_numerator = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)
    u = U_numerator/ denominator
    
    if t >= 0 and t <= 1 and u >= 0 and u <= 1:
        px = x1 + t * (x2 - x1)
        py = y1 + t * (y2 - y1)
        # OR
        # px = x3 + u * (x4 - x3)
        # py = y3 + u * (y4 - y3)
        return Vector(px, py)
    return None 



    



