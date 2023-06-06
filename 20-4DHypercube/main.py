import pygame
from constants import *
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("HYPERCUBE")
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
        self.scale = 4000
        self.position = [WIDTH//2, HEIGHT//2]

        self.points = [n for n in range(16)]

        self.points[0] = [[-1], [-1], [1], [1]]
        self.points[1] = [[1], [-1], [1], [1]]
        self.points[2] = [[1], [1], [1], [1]]
        self.points[3] = [[-1], [1], [1], [1]]
        self.points[4] = [[-1], [-1], [-1], [1]]
        self.points[5] = [[1], [-1], [-1], [1]]
        self.points[6] = [[1], [1], [-1], [1]]
        self.points[7] = [[-1], [1], [-1], [1]]
        self.points[8] = [[-1], [-1], [1], [-1]]
        self.points[9] = [[1], [-1], [1], [-1]]
        self.points[10] = [[1], [1], [1], [-1]]
        self.points[11] = [[-1], [1], [1], [-1]]
        self.points[12] = [[-1], [-1], [-1], [-1]]
        self.points[13] = [[1], [-1], [-1], [-1]]
        self.points[14] = [[1], [1], [-1], [-1]]
        self.points[15] = [[-1], [1], [-1], [-1]]
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            index = 0
            projected_points = [j for j in range(len(self.points))]

            for point in self.points:
                # Apply Transform 4D matrices
                transformed4D = matrix_multiplication(Rotation4dXY(self.angle), point)
                # transformed4D = matrix_multiplication(Rotation4dYZ(self.angle), transformed4D)
                transformed4D = matrix_multiplication(Rotation4dZW(self.angle), transformed4D)

                distance = 5
                z = 1/(distance - transformed4D[3][0])
                projected3D = matrix_multiplication(ProjectionMatrix4D(z), transformed4D)
                transformed3D = matrix_multiplication(TesseractRotation(), projected3D)
                
                # Apply Transform 3D matrices
                z = 1/(distance - (transformed3D[2][0] + transformed4D[3][0]))
                projected2D = matrix_multiplication(ProjectionMatrix(z), transformed3D)

                x = int(projected2D[0][0] * self.scale) + self.position[0]
                y = int(projected2D[1][0] * self.scale) + self.position[1]

                projected_points[index] = [x, y]
                pygame.draw.circle(self.screen, RED, (x, y), 10)
                index += 1

            # DRAW LINES FOR THE INNER CUBE
            for m in range(4):
                self.ConnectVertex(m, (m+1)%4, projected_points, 8)
                self.ConnectVertex(m+4, (m+1)%4+4, projected_points, 8)
                self.ConnectVertex(m, m+4, projected_points, 8)
            
            # DRAW LINES FOR THE OUTER CUBE
            for m in range(4):
                self.ConnectVertex(m, (m+1)%4, projected_points, 0)
                self.ConnectVertex(m+4, (m+1)%4+4, projected_points, 0)
                self.ConnectVertex(m, m+4, projected_points, 0)
            
            # DRAW LINES CONNECTING THE OUTER CUBE TO THE INNER CUBE
            for m in range(8):
                self.ConnectVertex(m, m+8, projected_points, 0)


            self.angle += SPEED
            if self.angle > math.pi*2:
                self.angle = 0
            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def ConnectVertex(self, i, j, points, offset):
        a = points[i + offset]
        b = points[j + offset]
        pygame.draw.line(self.screen, WHITE, (a[0], a[1]), (b[0], b[1]), 2)

        
if __name__ == "__main__":
    main()