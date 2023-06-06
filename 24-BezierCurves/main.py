import pygame
from constants import *
from position import Position
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BEZIER CURVE")
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
        self.font = font = pygame.font.SysFont('consolas', 32)
    
    def Run(self):
        t = 0
        linear_positions = [Position(100, 800, "P0"), Position(300, 200, "P1")]
        Quadratic_positions = [Position(660, 800, "P0"), Position(880, 450, "P1"), Position(720, 200, "P2")]
        cubic_positions = [Position(1050, 800, "P0"), Position(1280, 200, "P1"), Position(1420, 800, "P2"), Position(1800, 200, "P3")]

        quadratic_curve = []
        cubic_curve = []
        curve1 = []
        curve2 = []
        curve3 = []

        while self.running:
            self.screen.fill(BACKGROUND)
            self.HandleEvent()

            LinearCurve(linear_positions, t, self.screen, RED)
            QuadraticCurve(Quadratic_positions, t, self.screen, RED, quadratic_curve, BLUE)
            CubicCurve(cubic_positions, t, self.screen, RED, cubic_curve, GREEN, BLUE, curve1, curve2, curve3)
            
            if len(cubic_curve) > 2:
                pygame.draw.lines(self.screen, (179, 179, 179),False,  curve1, 3)
                pygame.draw.lines(self.screen, (179, 179, 179),False,  curve3, 3)
                pygame.draw.lines(self.screen, (179, 179, 179),False,  curve2, 3)
                pygame.draw.lines(self.screen, BLUE,False,  cubic_curve, 5)

            if len(quadratic_curve) > 2:
                pygame.draw.lines(self.screen, GREEN,False,  quadratic_curve, 5)

            # draw points
            for point in linear_positions:
                point.display(self.screen, RED)
            for point in Quadratic_positions:
                point.display(self.screen, BLUE)
            for point in cubic_positions:
                point.display(self.screen, BLUE)


            pygame.display.update()
            t+= SPEED
            if t > 1:
                t = 0
                quadratic_curve.clear()
                cubic_curve.clear()
                curve1.clear()
                curve2.clear()
                curve3.clear()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    

if __name__ == "__main__":
    main()