import pygame
import random
from constants import *
from ball import Ball
from paddle import Paddle

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping-Pong")
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
        self.background = pygame.image.load("./assets/BACKGROUND_PING_PONG.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.ball = Ball()
        self.left_paddle = Paddle(PADDLE_OFFSET)
        self.right_paddle = Paddle(WIDTH - PADDLE_OFFSET)
        
        self.left_score = 0
        self.right_score = 0
    
    def DrawScore(self):
        left_text = self.font.render(str(self.left_score), True, WHITE)
        self.screen.blit(left_text, (WIDTH//10, HEIGHT//12))
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(right_text, (WIDTH - 100, HEIGHT//12))
    def Run(self):
        while self.running:
            # self.screen.fill(BLACK)
            self.screen.blit(self.background, (0, 0))
            self.HandleEvent()

            self.ball.update()
            self.left_score, self.right_score = self.ball.Boundary(self.left_score, self.right_score)

            self.ball.Hit(self.left_paddle, True)
            self.ball.Hit(self.right_paddle, False)

            self.ball.Draw(self.screen)
            self.left_paddle.Draw(self.screen)
            self.right_paddle.Draw(self.screen)

            self.DrawScore()

            pygame.display.update()
            self.clock.tick(self.fps)
    
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            # LEFT paddle up
            self.left_paddle.update(-1 * PADDLE_SPEED)
            self.left_paddle.Boundary()
        elif key[pygame.K_s]:
            # LEFT paddle Down
            self.left_paddle.update(1 * PADDLE_SPEED)
            self.left_paddle.Boundary()
        if key[pygame.K_UP]:
            # RIGHT paddle up
            self.right_paddle.update(-1 * PADDLE_SPEED)
            self.right_paddle.Boundary()
        elif key[pygame.K_DOWN]:
            # RIGHT paddle Down
            self.right_paddle.update(1 * PADDLE_SPEED)
            self.right_paddle.Boundary()
                    

if __name__ == "__main__":
    main()