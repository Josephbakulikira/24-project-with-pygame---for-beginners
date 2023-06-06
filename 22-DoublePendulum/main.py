import pygame
from constants import *
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DOUBLE PENDULUM")
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

        self.x = WIDTH//2
        self.y = HEIGHT//2.8

        self.scatter1 = []
        self.scatter2 = []
    
    def Run(self):
        length1 = 200
        length2 = 200
        
        mass1 = 40
        mass2 = 40
        
        angle1 = math.pi/2
        angle2 = math.pi/2
        velocity1 = 0
        velocity2 = 0

        acceleration1 = 0
        acceleration2 = 0

        TraceLimit = 500
 
        while self.running:
            self.screen.fill(BLACK)
            self.clock.tick(self.fps)

            self.HandleEvent()

            if math.isinf(angle1):
                angle1 = 0
            if math.isinf(angle2):
                angle2 = 0

            acceleration1 = FirstAcceleration(angle1, angle2, mass1, mass2, length1, length2, GRAVITY, velocity1, velocity2)
            acceleration2 = SecondAcceleration(angle1, angle2, mass1, mass2, length1, length2, GRAVITY, velocity1, velocity2)

            # First Pendulum
            x1 = length1 * math.sin(angle1) + self.x 
            y1 = length1 * math.cos(angle1) + self.y

            # second Pendulum
            x2 = length2 * math.sin(angle2) + x1
            y2 = length2 * math.cos(angle2) + y1

            self.scatter1.insert(0, (x1, y1))
            self.scatter2.insert(0, (x2, y2))

            if len(self.scatter2) > TraceLimit:
                self.scatter1.pop()
                self.scatter2.pop()

            for i in range(len(self.scatter2)):
                # pygame.draw.circle(self.screen, WHITE, self.scatter2[i], 2)
                
                if i > 0:
                    pygame.draw.line(self.screen, GRAY, self.scatter2[i], self.scatter2[i-1], 1)

            # Draw Pendulums
            pygame.draw.line(self.screen, RED, (self.x, self.y), (x1, y1), 3)
            pygame.draw.line(self.screen, RED, (x1, y1), (x2, y2), 3)

            pygame.draw.circle(self.screen, GREEN, (x1, y1), mass1//2)
            pygame.draw.circle(self.screen, GREEN, (x2, y2), mass2//2)

            pygame.display.update()

            # update angle
            velocity1 += acceleration1
            velocity2 += acceleration2
            angle1 += velocity1
            angle2 += velocity2

            #Damping the velocity
            # angle1 *= 0.9
            # angle2 *= 0.9


    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    

if __name__ == "__main__":
    main()