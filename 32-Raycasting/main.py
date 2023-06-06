import pygame
import random
from constants import *
from wall import Wall
from particle import Particle

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RAY CASTING")
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

        self.walls = []
        offset = 25

        for i in range(5):
            ax = random.randint(offset, WIDTH - offset)
            bx = random.randint(offset, WIDTH - offset)
            ay = random.randint(offset, HEIGHT - offset)
            by = random.randint(offset, HEIGHT - offset)
            wall = Wall(ax, ay, bx, by)
            self.walls.append(wall)
        
        south_wall = Wall(offset, HEIGHT-offset, WIDTH-offset, HEIGHT-offset)
        north_wall = Wall(offset, offset, WIDTH-offset, offset)
        east_wall = Wall(WIDTH-offset, HEIGHT-offset, WIDTH-offset, offset)
        west_wall = Wall(offset, HEIGHT-offset, offset, offset)

        self.walls.append(south_wall)
        self.walls.append(north_wall)
        self.walls.append(east_wall)
        self.walls.append(west_wall)


        self.particle = Particle(WIDTH//2, HEIGHT//2)
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            dt = self.clock.tick(self.fps)
            self.HandleEvent()

            mx, my = pygame.mouse.get_pos()

            for wall in self.walls:
                wall.draw(self.screen)
            self.particle.update(self.screen, dt, mx, my, self.walls)
            # self.particle.draw(self.screen)

            
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