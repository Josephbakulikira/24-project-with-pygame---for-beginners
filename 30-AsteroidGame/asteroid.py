import pygame
from constants import *
from vector import Vector
from utils import WrapDisplay
import random

class Asteroid:
    def __init__(self, position, size):
        self.position = position
        self.velocity = Vector.Random(MIN_ASTEROID_SPEED, MAX_ASTEROID_SPEED)
        self.size = size

        self.thickness = 2
    
    def update(self, dt):
        self.position = self.position + self.velocity * dt
        self.Boundary()
    
    def Boundary(self):

        if self.position.x < 0:
            self.position.x = WIDTH
        elif self.position.x >= WIDTH:
            self.position.x = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
        elif self.position.y >= HEIGHT:
           self.position.y = 0

    def draw(self, screen):
        x, y = self.position.getTuple()
        pygame.draw.circle(screen, WHITE, (x, y), self.size, self.thickness)
        # WRAPPED
        x, y = WrapDisplay(self.position, self.size)
        
        pygame.draw.circle(screen, WHITE, (x, y), self.size, self.thickness)

def AsteroidSpawner(asteroid_list, spawn_size):
    for i in range(spawn_size):
        x, y = 0, 0
        x1 = random.randint(0, WIDTH//2 - ASTEROID_MAX_SIZE + PLAYER_SIZE + 10)
        x2 = random.randint( WIDTH//2 - ASTEROID_MAX_SIZE + PLAYER_SIZE + 10, WIDTH)

        y1 = random.randint(0, HEIGHT//2 - ASTEROID_MAX_SIZE + PLAYER_SIZE + 10)
        y2 = random.randint( HEIGHT//2 - ASTEROID_MAX_SIZE + PLAYER_SIZE + 10, HEIGHT)

        if random.randint(0, 100) > 50:
            x = x1
        else:
            x = x2
        if random.randint(0, 100) > 50:
            y = y1
        else:
            y = y2
        size = random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        asteroid = Asteroid(Vector(x, y), size)
        asteroid_list.append(asteroid)
    print(f"NEW WAVE -> {len(asteroid_list)}")
    