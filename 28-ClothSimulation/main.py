import pygame
from constants import *
from vector import Vector
from particle import Particle
from utils import *
from polygon import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CLOTH SIMULATION - VERLET INTEGRATION")
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
        self.isSelected = False
        self.selectedVertex = None
        self.selectedShape = None

        self.box = Box(Vector(WIDTH//5, HEIGHT//2), 100)
        self.rope = Rope(Vector(WIDTH//4, HEIGHT//2), 30, 10)
        self.cloth = Cloth(Vector(WIDTH//2-200, HEIGHT//6), 20, 10, 40, 4, 1, True, True, False, False)

        self.shapes= [self.cloth, self.box, self.rope]
    def Run(self):
        while self.running:
            # self.clock.tick(self.fps)
            dt = self.clock.tick(self.fps)
        
            self.screen.fill(BLACK)
            self.HandleEvent()

            for shape in self.shapes:
                shape.update(dt)
                shape.constraint()
                shape.draw(self.screen)

            pygame.display.update()
        
    def HandleEvent(self):
        mouse_select_area = 10
        mx, my = pygame.mouse.get_pos()
        mouse_pos = Vector(mx, my)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    if self.selectedVertex:
                        if self.selectedVertex in self.selectedShape.static:
                            self.selectedShape.static.remove(self.selectedVertex)
                        else:
                            self.selectedShape.static.append(self.selectedVertex)
                if event.key == pygame.K_s:
                    if self.selectedVertex:
                        self.selectedShape.DeconnectOne(self.selectedVertex)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.isSelected == False:
                    # Check all the particles in the area
                    found = False
                    for shape in self.shapes:
                        for vertex in shape.vertices:
                            if found == False and self.isSelected == False:
                                if Vector.GetDistance(mouse_pos, vertex.position) < mouse_select_area :
                                    vertex.isClicked = True
                                    self.isSelected = True
                                    self.selectedVertex = vertex
                                    self.selectedShape = shape
                                    found == True
                if event.button == 3 and self.isSelected == True:
                    self.isSelected = False
                    self.selectedVertex.isClicked = False
                    self.selectedVertex = None
                    self.selectedShape = None
                    found = False
            
    

if __name__ == "__main__":
    main()