import pygame
from constants import *
from vector import *

class Body:
    def __init__(self, position, mass, velocity, name="Default", color=(0, 0, 255), radius=20, history_limit=10):
        self.position = position
        self.mass = mass
        self.velocity = velocity
        self.acceleration = Vector2()
        self.color = color
        self.name = name
        self.radius = radius
        self.history = []
        self.history_limit = history_limit
    
    def Calculate(self, bodies):
        self.acceleration = Vector2()
        for body in bodies:
            if body == self:
                continue
            v = GetDistance2D(self.position, body.position)
            g_force = (self.mass * body.mass) / pow(v, 2)
            # Acceleration -> A = F/M
            acc = g_force / self.mass 
            diff = body.position - self.position
            self.acceleration = self.acceleration + diff.setMagnitude(acc)
    
    def Update(self, dt):
        self.velocity = self.velocity + (self.acceleration * dt)
        self.position = self.position + (self.velocity * dt)

        if len(self.history) > self.history_limit:
            self.history.pop()
        if self.name != "SUN":
            self.history.insert(0, self.position.ParseToInt())
    
    def Draw(self, screen, ShowTrail=True, isDotted=False):
        if ShowTrail:
            for i in range(len(self.history)):
                if i > 0 and isDotted == False:
                    pygame.draw.line(screen, self.color, self.history[i-1], self.history[i], LINE_THICKNESS)
                else:
                    pygame.draw.circle(screen, self.color, self.history[i], 2)
        pygame.draw.circle(screen, self.color, self.position.ParseToInt(), self.radius)
    
    def __repr__(self):
        #DEBUG
        return f"{self.name} -> position: {self.position}, velocity: {self.velocity}, mass : {self.mass}"