import pygame
from constants import *

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gCost = 0
        self.hCost = 0
        self.fCost = 0

        self.neighbours = []
        self.color = WHITE
        self.diagonal = False

        self.itsStart = False
        self.itsDestination = False
        self.itsObstacle = False

        self.distance = 0
        self.previous = None
    
    def updateNeighbours(self, nodes):
        x, y = self.x, self.y
        self.neighbours = []
        #right
        if x + 1 < len(nodes):
            self.neighbours.append(nodes[x+1][y])
        #left
        if x - 1 >= 0:
            self.neighbours.append(nodes[x-1][y])
        #bottom
        if y + 1 < len(nodes[0]):
            self.neighbours.append(nodes[x][y+1])
        #top
        if y - 1 >= 0:
            self.neighbours.append(nodes[x][y-1])

        if self.diagonal:
            #bottom-right
            if x + 1 < len(nodes) and y+1 < len(nodes[0]):
                self.neighbours.append(nodes[x + 1][y + 1])
            #top-right
            if x + 1 < len(nodes) and y-1 >= 0:
                self.neighbours.append(nodes[x + 1][y - 1])
            #bottom-left
            if x - 1 >= 0 and y + 1 <len(nodes[0]):
                self.neighbours.append(nodes[x - 1][y + 1])
            #top-left
            if x - 1 >= 0 and y - 1 >= 0:
                self.neighbours.append(nodes[x - 1][y - 1])

        return self.neighbours

    def Render(self, screen):
        scale = CELL_SIZE - CELL_OFFSET
        if self.itsStart:
            pygame.draw.rect(screen, GREEN, [self.x * CELL_SIZE , self.y * CELL_SIZE, scale, scale])
        elif self.itsDestination:
            pygame.draw.rect(screen, BLUE, [self.x * CELL_SIZE , self.y * CELL_SIZE, scale, scale])
        elif self.itsObstacle:
            pygame.draw.rect(screen, BLACK, [self.x * CELL_SIZE , self.y * CELL_SIZE, scale, scale])
        else:
            pygame.draw.rect(screen, self.color, [self.x * CELL_SIZE , self.y * CELL_SIZE, scale, scale])
