import pygame
from constants import *
from utils import *
from cell import *
from grid import *
from sidewinder import *
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MAZE GENERATOR")
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

        self.side_winder = SideWinder(Grid(), "BLUE")

        self.show_color_map = False
        self.show_heuristics = False
        self.show_path = True
    
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            self.side_winder.Generate(self.screen, self.show_heuristics, self.show_color_map, self.show_path)

            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_h:
                    self.show_heuristics = not self.show_heuristics
                elif event.key == pygame.K_s:
                    self.show_color_map = not self.show_color_map
                elif event.key == pygame.K_SPACE:
                    self.show_path = not self.show_path
    

if __name__ == "__main__":
    main()