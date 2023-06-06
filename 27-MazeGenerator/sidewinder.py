import pygame
import random
from constants import *
from grid import Grid, Update

class SideWinder:
    def __init__(self, grid, color_name):
        self.grid = grid
        self.isDone = False
        self.speed = 1
        self.color_name = color_name

        self.starting_node = grid.cells[0][0]
        self.starting_node.isStartingNode = True
        self.end_node = grid.cells[grid.cols-1][grid.rows-1]
        self.end_node.isgoalNode = True 

        self.shortest_path = None
        if color_name == "HSV":
            self.grid.path_color = WHITE

    def Generate(self, screen, show_heuristic, show_color_map, show_path):
        if not self.isDone:
            for y in range(self.grid.rows):
                history = []

                for x in range(self.grid.cols):
                    current = self.grid.cells[x][y]

                    current.isCurrent = True
                    history.append(current)
                    at_eastern_edge = False
                    at_northern_edge = False

                    if current.East == None:
                        at_eastern_edge = True
                    if current.North == None:
                        at_northern_edge = True

                    if at_eastern_edge or (at_northern_edge == False and random.randint(0, 1) == 1):
                        random_cell = random.choice(history)
                        if random_cell.North:
                            Grid.JoinAndDestroyWalls(random_cell, random_cell.North)
                        history.clear()
                    else:
                        Grid.JoinAndDestroyWalls(current, current.East)
                    
                    self.grid.Draw(screen, show_heuristic, show_color_map)
                    current.isCurrent = False
                    pygame.display.update()
            self.isDone = True
            Update(self, screen, show_heuristic, show_color_map, show_path)
        if show_path:
            self.grid.Draw(screen, show_heuristic, show_color_map, self.shortest_path)
        else:
            self.grid.Draw(screen, show_heuristic, show_color_map, None)

                    
    