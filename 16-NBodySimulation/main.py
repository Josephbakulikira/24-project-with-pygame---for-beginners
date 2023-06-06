import pygame
from constants import *
from body import *
from vector import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("N-BODY SIMULATION")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        self.count_ticks = 0
        self.running = True

        self.showDotted = False
        self.showTrail = True
        self.bodies = []

        #parameters
        self.Sun = Body(Vector2(WIDTH//2, HEIGHT//2), 100000, Vector2(), "Sun", (255, 255, 0), 100)

        self.Planet1 = Body(position=Vector2(WIDTH//2 + 200, HEIGHT//2  ),
                            mass=1,
                            velocity=Vector2(0, 25),
                            name="Planet1",
                            color=(0, 0, 255),
                            radius=20,
                            history_limit=400)
        self.Planet2 = Body(Vector2(WIDTH//2 - 300, HEIGHT//2 ), 1, Vector2(0, 15), "Planet2", (0, 255, 255), 15, 400)
        self.Planet3 = Body(Vector2(WIDTH//2 - 380, HEIGHT//2 ), 1, Vector2(0, 15), "Planet2", (25, 155, 255), 20, 400)
        self.Planet4 = Body(Vector2(WIDTH//2 + 400, HEIGHT//2  ), 2, Vector2(0, 17), "Planet2", (220, 55, 55), 40, 400)

        self.bodies.append(self.Sun)
        self.bodies.append(self.Planet1)
        self.bodies.append(self.Planet2)
        self.bodies.append(self.Planet3)
        self.bodies.append(self.Planet4)

        self.last_ticks = 0 # previous milliseconds
        self.count_ticks = 0
    
    def Run(self):
        while self.running:
            # delta time
            # # Get the delta Time since the last frame update
            ticks        = pygame.time.get_ticks()
            ticksElapsed = ticks - self.last_ticks
            s_ticks    = ticksElapsed/1000
            self.last_ticks   = ticks

            self.count_ticks += s_ticks

            self.screen.fill(BLACK)
            self.HandleEvent()

            self.count_ticks += s_ticks
            # For an accurate approximation you can use time step instead of just a simple loop
            while self.count_ticks > STEP:
                for body in self.bodies:
                    body.Calculate(self.bodies)
                for body in self.bodies:
                    body.Update(STEP * SPEED)
                
                self.count_ticks -= STEP
            
            for body in self.bodies:
                body.Draw(self.screen, self.showTrail, self.showDotted)
        
            pygame.display.update()
            self.clock.tick(self.fps)
    
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_t:
                    self.showTrail = not self.showTrail
                if event.key == pygame.K_d:
                    self.showDotted = not self.showDotted

if __name__ == "__main__":
    main()
