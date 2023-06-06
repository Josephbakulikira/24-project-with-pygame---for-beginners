import pygame
from ray import Ray
import utils
from constants import *
from vector import Vector
import math

class Particle:
    def __init__(self, x, y):
        self.position = Vector(x, y)
        self.steps = 10
        self.rays = []
        # initialize rays
        for i in range(0, 360):
            angle = math.radians(i)
            self.rays.append(Ray(self.position, angle))
    
    def update(self, screen, dt, mx, my, walls):
        self.position.x = mx
        self.position.y = my
        for ray in self.rays:
            closest = None
            record = 50000

            for wall in walls:
                p = ray.Cast(wall)
                if p:
                    dist = Vector.GetDistance(self.position, p)
                    if dist < record:
                        record = dist
                        closest = p
            if closest:
                pygame.draw.line(screen, WHITE, self.position.getTuple(), closest.getTuple(), 1)
                    

                    

    def draw(self, screen):
        # DRAW THE RAYS
        # for ray in self.rays:
        #     ray.draw(screen)
        pygame.draw.circle(screen, WHITE, self.position.getTuple(), 5)
        
        