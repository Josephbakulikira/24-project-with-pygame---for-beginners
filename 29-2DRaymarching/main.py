import pygame
from constants import *

from obstacles import Obstacle
from ray import Ray
from random import randint

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D - RAYMARCHING")
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

        self.obstacles = []
        self.collisions = []

        for i in range(10):
            x = randint(50, WIDTH-50)
            y = randint(50, HEIGHT-50)
            r = randint(20, 100)
            obj = Obstacle(x, y, r)
            obj.color = (0, 0, 0)
            obj.outline = 0
            self.obstacles.append(obj)
        
        self.auto_rotation = True
        self.angle = 0
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.angle -= 0.008
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.angle += 0.008
            
            mx, my = pygame.mouse.get_pos()
            ray = Ray(mx, my, 0, WHITE)
            ray.angle = self.angle
            
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            for p in self.collisions:
                pygame.draw.circle(self.screen, WHITE, p, 2)
            
            if len(self.collisions) > 500:
                self.collisions.pop()

            ray.March(self.obstacles, self.collisions, self.screen)

            if self.auto_rotation == True:
                self.angle += 0.002

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