import pygame
from vector import Vector
from constants import *

class Particle:
    def __init__(self, position, radius=5, color=WHITE):
        self.position = position
        self.oldPosition = position - Vector(0, -1)
        self.radius = radius
        self.color = color
        self.mass = 1000
        
        self.isClicked = False
    
    def update(self, dt):
        # Compute velocity
        force = Vector(0.0, GRAVITY)
        # F = M x A -- > A = F/M
        acceleration = force/self.mass
        acceleration = acceleration * (dt*dt)
        old_position = self.position.copy()

        p = self.position * 2
        difference = p - self.oldPosition
        self.position = difference + acceleration

        self.oldPosition = old_position
        self.boundary()
    
    def boundary(self):
        vel = self.position - self.oldPosition

        if self.position.x < self.radius:
            self.position.x = self.radius
            self.oldPosition.x = self.position.x + vel.x
        if self.position.x > WIDTH-self.radius:
            self.position.x = WIDTH - self.radius
            self.oldPosition.x = self.position.x + vel.x
        
        if self.position.y < self.radius:
            self.position.y = self.radius
            self.oldPosition.y = self.position.y + vel.y
        if self.position.y > HEIGHT - self.radius:
            self.position.y = HEIGHT - self.radius
            self.oldPosition.y = self.position.y + vel.y

    def draw(self, screen):
        if self.isClicked:
            color = RED
        else:
            color = self.color
        pygame.draw.circle(screen, color, self.position.getTuple(), self.radius)

