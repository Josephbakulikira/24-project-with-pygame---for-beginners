import pygame
import math
from constants import *
from vector import Vector
from utils import *

class Player:
    def __init__(self, position, angle):
        self.position = position
        self.angle = angle
        self.velocity = Vector()

        self.steerForce = PLAYER_STEER_FORCE
        self.thrustSpeed = PLAYER_THRUST_FORCE
        self.size = PLAYER_SIZE

        self.front = Vector.fromAngle(self.angle, self.size/1.5) + position
        self.backRight = Vector.fromAngle(self.angle - math.pi//2 - math.pi, self.size//2) + position
        self.backLeft = Vector.fromAngle(self.angle + math.pi//2 - math.pi, self.size//2) + position
    
    def update(self, dt):
        self.HandleInput(dt)
        # self.UpdatePlayerAngle()
        # Limit player speed
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

        self.velocity = Vector.Limit(self.velocity, MAX_PLAYER_SPEED)

        self.UpdateTriangle()
        self.Boundary()
    
    def UpdateTriangle(self):
        self.front = Vector.fromAngle(self.angle, self.size/1.5) + self.position
        self.backRight = Vector.fromAngle(self.angle - math.pi//2 - math.pi, self.size//2) + self.position
        self.backLeft = Vector.fromAngle(self.angle + math.pi//2 - math.pi, self.size//2) + self.position
    
    def UpdatePlayerAngle(self):
        mx, my = pygame.mouse.get_pos()
        newX = mx - WIDTH//2
        newY = my - HEIGHT//2
        vec = Vector(-newY, newX)
        self.angle = Vector.Heading(vec)
        
    
    def Boundary(self):
        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x >= WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y >= HEIGHT:
           self.position.y = 0

    def HandleInput(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.x += math.sin(self.angle) * self.thrustSpeed * dt
            self.velocity.y += -math.cos(self.angle) * self.thrustSpeed * dt

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.steerForce * dt
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.steerForce * dt

    def draw(self,screen, color=WHITE):
        x, y = self.position.getTuple()

        # pygame.draw.circle(screen, color, (x, y), self.size)
        DrawTriangle(screen, self.position, self.front, self.backLeft, self.backRight, self.angle, self.size, color, False)
        # WRAPPED
        x, y = WrapDisplay(self.position, self.size)
        DrawTriangle(screen, Vector(x, y), self.front, self.backLeft, self.backRight, self.angle, self.size, color, False)

        # COLLISION CIRCLE 
        # pygame.draw.circle(screen, GRAY, self.position.getTuple(), self.size/1.3, 2)