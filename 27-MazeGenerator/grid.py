from constants import *
from cell import Cell
import pygame
from color import GridColor

class Grid:
    def __init__(self, rows=ROWS, cols=COLS, cell_size=CELL_SIZE):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Initiliaze cells
        self.cells = [[Cell(x, y) for y in range(rows)] for x in range(cols)]
        self.PrepareGrid()

        self.heuristics = None
        self.path_color = RED
        self.isSorted = False

        self.path = {}
        self.path_values = []

    def Flatten(self):
        flat_grid = []

        for x in range(self.cols ):
            for y in range(self.rows):
                if self.cells[x][y]:
                    flat_grid.append(self.cells[x][y])
        return flat_grid
    
    def PrepareGrid(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.cells[x][y]:
                    self.cells[x][y].neighbours = []
                    # EAST NEIGHBOUR CELL
                    if x + 1 < self.cols and self.cells[x+1][y]:
                        self.cells[x][y].East = self.cells[x+1][y]
                        self.cells[x][y].neighbours.append(self.cells[x+1][y])
                    # WEST NEIGHBOUR CELL
                    if x - 1 >= 0 and self.cells[x-1][y]:
                        self.cells[x][y].West = self.cells[x-1][y]
                        self.cells[x][y].neighbours.append(self.cells[x-1][y])
                    # NORTH NEIGHBOUR CELL
                    if y-1 >= 0 and self.cells[x][y-1]:
                        self.cells[x][y].North = self.cells[x][y-1]
                        self.cells[x][y].neighbours.append(self.cells[x][y-1])
                    # SOUTH NEIGHBOUR CELL
                    if y+1 < self.rows and self.cells[x][y+1]:
                        self.cells[x][y].South = self.cells[x][y+1]
                        self.cells[x][y].neighbours.append(self.cells[x][y+1])
    
    def JoinAndDestroyWalls(A, B):
        if A.isAvailable and B.isAvailable:
            A.visited = True
            B.visited = True
            A.connections.append(B)
            B.connections.append(A)

            if A.North == B:
                A.North, B.South = None, None
            elif A.South == B:
                A.South, B.North = None, None
            elif A.East == B:
                A.East, B.West = None, None
            elif A.West == B:
                A.West, B.East = None, None

    def Draw(self, screen, show_heuristic, show_color_map, shortest_path = None):
        if not self.isSorted and shortest_path:
            for x in range(self.cols):
                for y in range(self.rows):
                    if shortest_path.cells_record[x][y]:
                        val = shortest_path.cells_record[x][y]
                        self.path_values.append(val)
                        self.path[str(val)] = ((x+0.5) * CELL_SIZE, (y+0.5) * CELL_SIZE)
            self.path_values = sorted(self.path_values)
            self.isSorted = True


        for x in range(self.cols):
            for y in range(self.rows):
                if self.cells[x][y]:
                    self.cells[x][y].show_text = show_heuristic
                    self.cells[x][y].show_highlight = show_color_map
                    self.cells[x][y].Draw(screen, self.rows, self.cols)

        if shortest_path:
            for i in range(len(self.path_values)-1):
                pygame.draw.line(screen, RED, self.path[str(self.path_values[i])], self.path[str(self.path_values[i+1])], 2)
                pygame.draw.circle(screen, RED, self.path[str(self.path_values[i])], self.cell_size//6)
            

def Update(algorithm, screen, show_heuristic, show_color_map, show_path):
    this = algorithm
    # Calculate the step of each cell from the starting node
    # it's gonna initialize a grid that store the cost of each cell
    # from the starting node
    h_distances = this.starting_node.CalculateHeuristic(this.grid.rows, this.grid.cols)
    this.grid.heuristics = h_distances
    for x in range(len(this.grid.cells)):
        for y in range(len(this.grid.cells[x])):
            if this.grid.cells[x][y]:
                this.grid.cells[x][y].cost = 0 if this.grid.heuristics.cells_record[x][y] == None else this.grid.heuristics.cells_record[x][y]
    
    # Get The path from the goal node to the starting node
    shortest_path = h_distances.BacktrackPath(this.end_node, this.starting_node)
    for x in range(this.grid.cols):
        for y in range(this.grid.rows):
            if this.grid.cells[x][y]:
                # Check if the cell is in the path grid
                # If it is then set it as path
                if shortest_path.GetRecord(this.grid.cells[x][y]):
                    this.grid.cells[x][y].isPath = True
    
    colorGridShortestPath = GridColor(this.color_name)
    colorGridShortestPath.distances(shortest_path, this.end_node, this.starting_node, this.grid)
    temp_path = h_distances.Merge(shortest_path)

    colorGridMap = GridColor(this.color_name)
    colorGridMap.distances(temp_path, this.end_node, this.starting_node, this.grid)

    for x in range(this.grid.cols):
        for y in range(this.grid.rows):
            if this.grid.cells[x][y]:
                this.grid.cells[x][y].highlight = colorGridShortestPath.UpdateColor(this.grid.cells[x][y])
                this.grid.cells[x][y].color = colorGridMap.UpdateColor(this.grid.cells[x][y])

                this.grid.Draw(screen, show_heuristic, show_color_map)
                pygame.display.update()
    
    this.shortest_path = shortest_path

