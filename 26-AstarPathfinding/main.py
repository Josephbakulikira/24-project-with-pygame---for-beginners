import pygame
from constants import *
from cell import Cell
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ASTAR PATHFINDING")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.fps = 60

        self.cols = HEIGHT//CELL_SIZE
        self.rows = WIDTH//CELL_SIZE

        self.grid = [[Cell(j, i) for i in range(self.cols)] for j in range(self.rows)]
        self.path = []

        self.closedSet = []
        self.openSet = []
        self.diagonalToggle = False

        for x in range(self.rows):
            for y in range(self.cols):
                self.grid[x][y].diagonal = self.diagonalToggle
                self.grid[x][y].updateNeighbours(self.grid)
        
        self.startNode = self.grid[3][self.cols//2]
        self.startNode.itsStart = True
        self.goalNode = self.grid[self.rows-3][self.cols//2]
        self.goalNode.itsDestination = True
        self.openSet.append(self.startNode)

        self.finished = False
        self.pause = True

        self.currentNode = self.startNode

    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            if not self.pause:
                if len(self.openSet) > 0 and self.finished == False:
                    winner = 0
                    for i in range(len(self.openSet)):
                        # Set the winner as the one with the least f Cost
                        if self.openSet[i].fCost < self.openSet[winner].fCost:
                            winner = i
                        # In case of a tie of fcost
                        if self.openSet[i].fCost == self.openSet[winner].fCost:
                            # Compare their gCost
                            if self.openSet[i].gCost > self.openSet[winner].gCost:
                                winner = i
                        if self.diagonalToggle == False:
                            if self.openSet[i].gCost == self.openSet[winner].gCost \
                                and self.openSet[i].distance == self.openSet[winner].distance:
                                winner = i
                    self.currentNode = self.openSet[winner]

                    # Check if we're done
                    if self.currentNode == self.goalNode:
                        self.finished = True
                    # Remove the current node from the open set
                    self.openSet.remove(self.currentNode)
                    self.closedSet.append(self.currentNode)

                    neighbours = self.currentNode.updateNeighbours(self.grid)
                    # check the neighbours nodes
                    for neighbour in neighbours:
                        if neighbour not in self.closedSet and neighbour.itsObstacle == False:
                            dist = euclideanDistance(neighbour, self.currentNode)
                            cost = self.currentNode.gCost + dist
                            # Check it it's better than the route before
                            if neighbour not in self.openSet:
                                self.openSet.append(neighbour)
                            elif cost >= neighbour.gCost:
                                continue
                            neighbour.gCost = cost
                            neighbour.hCost = euclideanDistance(neighbour, self.goalNode)

                            if self.diagonalToggle == False:
                                neighbour.distance = euclideanDistance(neighbour, self.goalNode)
                            neighbour.fCost = neighbour.gCost + neighbour.hCost
                            neighbour.previous = self.currentNode
                            neighbour.previous.color = PURPLE

            for x in range(self.rows):
                for y in range(self.cols):
                    self.grid[x][y].Render(self.screen)
            
            self.path = []
            tempNode = self.currentNode
            self.path.append(tempNode)

            while tempNode.previous:
                self.path.append(tempNode.previous)
                tempNode = tempNode.previous

            for cell in self.openSet:
                cell.color = GREEN
            
            for cell in self.closedSet:
                c = pygame.Color(0, 0, 0)
                c.hsva = (((cell.x + cell.y) + 230)%360, 100, 100, 100)
                cell.color = c
            
            for cell in self.path:
                cell.color = PURPLE
            
            if self.finished:
                if len(self.path) > 1:
                    for i in range(1, len(self.path)):
                        x1 = self.path[i].x * CELL_SIZE + CELL_SIZE//2
                        y1 = self.path[i].y * CELL_SIZE + CELL_SIZE//2
                        x2 = self.path[i-1].x * CELL_SIZE + CELL_SIZE//2
                        y2 =self.path[i-1].y * CELL_SIZE + CELL_SIZE//2
                        pygame.draw.line(self.screen, WHITE, (x1, y1), (x2, y2), 2)

            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                elif event.key == pygame.K_r:
                    self.finished = False
                    self.grid = [[Cell(j, i) for i in range(self.cols)] for j in range(self.rows)]
                    self.path.clear()

                    self.closedSet.clear()
                    self.openSet.clear()

                    for x in range(self.rows):
                        for y in range(self.cols):
                            self.grid[x][y].diagonal = self.diagonalToggle
                            self.grid[x][y].updateNeighbors(self.grid)

                    self.startNode   = self.grid[3][self.cols//2]
                    self.startNode.itsObstacle = False
                    self.startNode.itsStart = True
                    self.goalNode    = self.grid[self.rows-3][self.cols//2]
                    self.goalNode.itsObstacle = False
                    self.goalNode.color = (0, 0, 255)
                    self.goalNode.itsDestination = True

                    self.openSet.append(self.startNode)
                    self.pause = True
        
        mx, my = pygame.mouse.get_pos()
        x = mx//CELL_SIZE
        y = my//CELL_SIZE

        if pygame.mouse.get_pressed()[0] == 1:
            if self.grid[x][y].itsDestination == False \
                and self.grid[x][y].itsStart == False:
                self.grid[x][y].itsObstacle = True
        elif pygame.mouse.get_pressed()[2] == 1:
            self.grid[x][y].itsObstacle = False
    

if __name__ == "__main__":
    main()