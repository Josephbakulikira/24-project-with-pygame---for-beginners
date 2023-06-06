from constants import *
from utils import *
from vector import *

class Bullet:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.size = BULLET_SIZE
        self.color = WHITE
    
    def update(self, dt):
        self.position = self.position + self.velocity * dt

    def offScreen(self):
        if self.position.x < 0:
            return True
        elif self.position.x >= WIDTH:
            return True
        if self.position.y < 0:
            return True
        elif self.position.y >= HEIGHT:
           return True
        
        return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position.getTuple(), self.size)
    
    