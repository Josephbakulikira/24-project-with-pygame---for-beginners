import pygame
from constants import *
from heuristic import Heuristic

pygame.font.init()
text_font = pygame.font.SysFont("consolas", CELL_SIZE//3)
offset = 0

class Cell:
    def __init__(self, x, y, size=CELL_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.color = WHITE

        self.cost = 0
        self.isGoalNode = False
        self.isStartingNode = False
        self.isCurrent = False
        self.isPath = False
        self.show_path = False

        self.wall_color = BLACK
        self.wall_thickness = 4
        self.visited = False
        self.connections = []
        self.neighbours = []
        self.isAvailable = True

        # WALLS -- NEIGHBOURS
        self.North = None
        self.South = None
        self.East = None
        self.West = None

        self.show_text = True
        self.text_color = (0 , 0, 0)
        self.show_highlight = False
        self.highlight = WHITE

    def CalculateHeuristic(self, rows, cols):
        h_distance = Heuristic(rows, cols)
        frontier = [self]
        while len(frontier) > 0:
            new_frontier = []
            for c in frontier:
                for cell in c.connections:
                    if h_distance.GetRecord(cell):
                        continue
                    val = 0 if h_distance.GetRecord(c) == None else h_distance.GetRecord(c)
                    h_distance.SetRecord(cell, val+1)
                    new_frontier.append(cell)
            frontier = new_frontier
        h_distance.SetRecord(self, 0)
        return h_distance

    def Draw(self, screen, rows, cols):
        x = self.x * self.size
        y = self.y * self.size

        if not self.visited or not self.isAvailable:
            pygame.draw.rect(screen, BLACK, [x, y, self.size, self.size])
        else:
            color = self.color
            if self.isStartingNode:
                color = GREEN
            elif self.isGoalNode:
                color = BLUE
            if self.isCurrent:
                color = PURPLE
            pygame.draw.rect(screen, color, [x, y, self.size, self.size])

            if self.show_highlight:
                pygame.draw.rect(screen, self.highlight, [x, y, self.size, self.size])

        # DRAW WALLS
        if self.North!= None or self.y - 1 < 0:
            A = (x, y)
            B = (x + self.size, y)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.South != None or self.y + 1 >= rows:
            A = (x, y + self.size)
            B = (x+self.size, y+self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.East != None or self.x + 1 >= cols:
            A = (x + self.size, y)
            B = (x + self.size, y+self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        if self.West != None or self.x - 1 < 0:
            A = (x, y)
            B = (x, y + self.size)
            pygame.draw.line(screen, self.wall_color, A, B, self.wall_thickness)
        

        if self.show_text:
            text_surface = text_font.render(str(int(self.cost)), True, self.text_color)
            text_rect = text_surface.get_rect(center=(x+self.size//2, y + self.size//2))
            screen.blit(text_surface, text_rect)
            
