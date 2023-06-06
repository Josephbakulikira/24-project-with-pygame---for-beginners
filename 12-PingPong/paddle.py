import pygame
from constants import *

class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT//2
        self.height = 140
        self.width = 20 
        self.color = WHITE
    
    def update(self, offset):
        self.y += offset
        self.Boundary()
    
    def Boundary(self):
        if self.y - self.height//2 <= 0:
            self.y = self.height//2
        elif self.y + self.height//2 >= HEIGHT:
            self.y = HEIGHT - self.height//2
    
    def Draw(self, screen):
        # ANCHOR on the top left corner
        pos_x = self.x - self.width//2
        pos_y = self.y - self.height//2
        pygame.draw.rect(screen, self.color, [pos_x, pos_y, self.width, self.height])
    
    
    