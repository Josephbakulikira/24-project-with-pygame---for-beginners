import pygame
from constants import *
import colorsys
import math

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Times table Cardioid")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

    pygame.quit()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        self.running = True
        
        self.max_points = 200
        self.n_point = 100
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.radius = 500
        self.factor = 0
        
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            self.HandleEvent()

            # DRAW the main Circle
            pygame.draw.circle(self.screen, WHITE, (self.x, self.y), self.radius, 1)

            # Map the number of points based on the x position of the mouse on the screen
            mouse_x , _ = pygame.mouse.get_pos()
            self.n_point = int(translate(mouse_x, 0, WIDTH, 0, self.max_points))
            
            for i in range(self.n_point):
                a, b = self.GetPosition(i)
                v, w = self.GetPosition(i * self.factor)
                # Draw line between the connected point
                pygame.draw.line(self.screen, hsv2rgb(self.factor, 1, 1), (a + self.x, b + self.y), (v + self.x, w + self.y), 1)
            
            for i in range(self.n_point):
                # draw n amount of points around our main circle
                a, b = self.GetPosition(i)
                pygame.draw.circle(self.screen, WHITE, (a + self.x, b + self.y), 10)
                
            self.factor += ANIMATION_SPEED
            # self.hue += ANIMATION_SPEED

            pygame.display.update()
            self.clock.tick(self.fps)

    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def GetPosition(self, n):
        # return translated polar coordinate
        theta = translate(n % self.n_point, 0, self.n_point, 0, math.pi * 2)
        theta += math.pi
        a = self.radius * math.cos(theta)
        b = self.radius * math.sin(theta)
        return a, b

def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2) * ( (value - min1) / (max1 - min1))

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))



if __name__ == "__main__":
    main()