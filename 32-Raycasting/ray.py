import pygame
from vector import *
from constants import *
from utils import *

class Ray:
    def __init__(self, position, angle):
        self.position = position
        self.direction = Vector.fromAngle(angle)
        # self.pointB = self.position + self.direction * 500
        self.color = YELLOW

    def LookAt(self, x, y):
        self.direction = Vector(x, y) - self.position
        self.direction = self.direction.normalize()
        # self.pointB = self.position + self.direction * 500
        
    def Cast(self, line):
        a = self.position
        b = self.position + (self.direction * (WIDTH+HEIGHT))
        c = line.a
        d = line.b

        return LineLineIntersection(a, b, c, d)
        
    def draw(self, screen):
        a = self.position.getTuple()
        b = (self.position + self.direction * WIDTH ).getTuple()
        pygame.draw.circle(screen, self.color, a, 4)
        pygame.draw.line(screen, self.color, a, b, LINE_THICKNESS)