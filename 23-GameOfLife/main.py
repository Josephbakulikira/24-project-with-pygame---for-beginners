import pygame
from constants import *
from grid import Grid

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CONWAY'S GAME OF LIFE")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.fps = 30

        self.grid = Grid()
        self.grid.Random2DArray()

        self.pause = False
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            self.grid.Conway(self.screen, self.pause)

            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                self.grid.HandleMouse(mx, my)

            pygame.display.update()
            self.clock.tick(self.fps)
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
    

if __name__ == "__main__":
    main()