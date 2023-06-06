import pygame
from constants import *
import math

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("FOURIER SERIES")
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

        self.time = 0
        self.position = [400, HEIGHT//2]
        self.pointList = []
        self.radius = 0
        self.offset = 300
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            x = self.position[0]
            y = self.position[1]

            for i in range(ITERATIONS):
                oldX = x
                oldY = y

                N = i * 2 + 1
                self.radius = 150 * (5/(N*math.pi))
                # Polar coordinates
                x += int(self.radius * math.cos(N*self.time))
                y += int(self.radius * math.sin(N*self.time))

                pygame.draw.circle(self.screen, WHITE, (oldX, oldY), int(self.radius), 2)

                pygame.draw.line(self.screen, WHITE, (oldX, oldY), (x, y), 3)
                pygame.draw.circle(self.screen, GREEN, (x, y), 5)

            self.pointList.insert(0, y)
            if len(self.pointList) > 1000:
                self.pointList.pop()
            
            pygame.draw.line(self.screen, GRAY, (x, y), (self.position[0] + self.offset, self.pointList[0]), 3)

            for index in range(len(self.pointList)):
                pygame.draw.circle(self.screen, WHITE, (index + self.position[0] + self.offset, self.pointList[index]), 3)

            self.time += 0.01
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