import pygame
from constants import *
from utils import *
import math

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LISSAJOUS CURVE TABLE")
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
        self.w = 140
        self.restart = False
        self.hue = 0

        self.cols = WIDTH//self.w-1
        self.rows = HEIGHT//self.w-1

        
        self.radius = int((self.w//2) - 0.1*self.w)
        self.curves = [[i for i in range(self.cols)] for j in range(self.rows)]

        for x in range(self.rows):
            for y in range(self.cols):
                self.curves[x][y] = Curve(hsv_to_rgb(self.hue, 1, 1))
                self.hue += 0.001
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            for i in range(self.cols):
                a = self.w+10 + i * self.w + self.w // 2
                b = self.w//2 + 15
                pygame.draw.circle(self.screen, WHITE, (a, b), int(self.radius), 1)

                x = self.radius * math.sin(self.angle * (i+1) - math.pi/2)
                y = self.radius * math.cos(self.angle * ( i + 1) - math.pi/2)

                pygame.draw.line(self.screen, GRAY, (int(a+x), 0), (int(a+x), HEIGHT), 1)
                pygame.draw.circle(self.screen, WHITE, (int(a+x), int(b+y)), 8)

                for j in range(self.rows):
                    self.curves[j][i].set_point_x(a+x)
            
            for j in range(self.rows):
                a = self.w //2 + 15
                b = self.w + 10 + j * self.w + self.w//2
                pygame.draw.circle(self.screen, WHITE, (a, b), self.radius, 1)

                x = self.radius * math.sin(self.angle * (j+1) - math.pi//2)
                y = self.radius * math.cos(self.angle * (j+1) - math.pi//2)

                pygame.draw.line(self.screen, GRAY, (0, int(b+y)), (WIDTH, int(b+y)), 1)
                pygame.draw.circle(self.screen, WHITE, (int(a+x), int(b+y)), 8)

                for i in range(self.cols):
                    self.curves[j][i].set_point_y(b+y)

            for x in range(self.rows):
                for y in range(self.cols):
                    self.curves[x][y].update_points()
                    self.curves[x][y].draw(self.screen)

            self.angle += SPEED
            if self.angle > math.pi * 2 or self.restart == True:
                for x in range(self.rows):
                    for y in range(self.cols):
                        self.curves[x][y].points = []
            
            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.restart = True
    

if __name__ == "__main__":
    main()