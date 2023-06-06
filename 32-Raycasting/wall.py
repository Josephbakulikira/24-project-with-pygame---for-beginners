import pygame
from vector import Vector
from constants import *

class Wall:
    def __init__(self, ax, ay, bx, by):
        self.a = Vector(ax, ay)
        self.b = Vector(bx, by)
        self.color = WHITE
        self.thickness = LINE_THICKNESS
    
    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.a.getTuple(), self.b.getTuple(), self.thickness)
