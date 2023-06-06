import pygame
import random 
from constants import *

class Grid:
    def __init__(self):
        self.scale = SCALE

        self.cols = HEIGHT//SCALE
        self.rows = WIDTH//SCALE

        self.size = (self.rows, self.cols)
        self.grid_array = [[ 0 for i in range(self.cols)] for j in range(self.rows)]
        self.offset = OFFSET
    
    def Random2DArray(self):
        for x in range(self.rows):
            for y in range(self.cols):
                self.grid_array[x][y] = random.randint(0, 1)
    
    def Conway(self, screen, pause):
        for i in range(self.rows):
            for j in range(self.cols):
                y = j * self.scale
                x = i * self.scale

                if self.grid_array[i][j] == 1:
                    pygame.draw.rect(screen, ON_COLOR, [x, y, self.scale-self.offset, self.scale-self.offset])
                else:
                    pygame.draw.rect(screen, OFF_COLOR, [x, y, self.scale-self.offset, self.scale-self.offset])
    
        next = [[ 0 for i in range(self.cols)] for j in range(self.rows)]
        if pause == False:
            for x in range(self.rows):
                for y in range(self.cols):
                    state = self.grid_array[x][y]
                    neighbours = self.GetNeighbours(x, y)
                    if state == 0 and neighbours == 3:
                        next[x][y] = 1
                    elif state == 1 and (neighbours < 2 or neighbours > 3):
                        next[x][y] = 0
                    else:
                        next[x][y] = state
            self.grid_array = next

    def HandleMouse(self, x, y):
        dx = x // self.scale
        dy = y // self.scale

        if self.grid_array[dx][dy] != None:
            self.grid_array[dx][dy] = 1
    
    def GetNeighbours(self, x, y):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                dx = (x + i + self.rows) % self.rows
                dy = (y + j + self.cols) % self.cols
                total += self.grid_array[dx][dy]
        total -= self.grid_array[x][y]
        return total
