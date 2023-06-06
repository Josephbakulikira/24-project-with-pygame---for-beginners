import pygame
import math

from constants import *
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PERSPECTIVE PROJECTION")
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

        self.angle = 0
        self.position = [WIDTH//2, HEIGHT//2]
        self.scale = 600
        speed = 0.01

        self.points = [None for n in range(8)]
        self.points[0] = [[-1], [-1], [1]]
        self.points[1] = [[1], [-1], [1]]
        self.points[2] = [[1], [1], [1]]
        self.points[3] = [[-1], [1], [1]]

        self.points[4] = [[-1], [-1], [-1]]
        self.points[5] = [[1], [-1], [-1]]
        self.points[6] = [[1], [1], [-1]]
        self.points[7] = [[-1], [1], [-1]]


    def ConnectVertex(self, i, j, points):
        a = points[i]
        b = points[j]
        pygame.draw.line(self.screen, WHITE, (a[0], a[1]), (b[0], b[1]), 2)

    def Run(self):
        while self.running:
            self.screen.fill(BLACK)

            self.HandleEvent()

            index = 0
            projected_points = [j for j in range(len(self.points))]
            
            for point in self.points:
                transformed = matrix_multiplication(RotationX(self.angle), point)
                transformed = matrix_multiplication(RotationY(self.angle), transformed)
                transformed = matrix_multiplication(RotationZ(self.angle), transformed)

                distance = 5
                z = 1/(distance - transformed[2][0])
                p_mat = ProjectionMatrix(z)
                projected = matrix_multiplication(p_mat, transformed)

                x = int(projected[0][0] * self.scale) + self.position[0]
                y = int(projected[1][0] * self.scale) + self.position[1]
                projected_points[index] = [x, y]
                pygame.draw.circle(self.screen, GREEN, (x, y), 10)
                index += 1

            self.angle += SPEED
            if self.angle > math.pi * 2:
                self.angle = 0
            
            # DRAW EDGES
            for m in range(4):
                self.ConnectVertex(m, (m+1)%4, projected_points)
                self.ConnectVertex(m+4, (m+1)%4+4, projected_points)
                self.ConnectVertex(m, m+4, projected_points)

            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    

if __name__ == "__main__":
    main()