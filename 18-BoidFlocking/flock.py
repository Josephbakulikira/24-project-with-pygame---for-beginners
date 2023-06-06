from boid import Boid
from constants import *
import random


class Flock:
    def __init__(self):
        self.boids = []
    
    def Setup(self, size):
        for _ in range(size):
            x = random.randint(20, WIDTH-20)
            y = random.randint(20, HEIGHT-20)
            self.Push(Boid(x, y))
    
    def Run(self, screen):
        for boid in self.boids:
            boid.run(self.boids, screen)
    
    def Push(self, boid):
        
        self.boids.append(boid)