import pygame
import random

# CONSTANTS
WIDTH = 800
HEIGHT = 800
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (80, 255, 100)
RED = (255, 120, 10)
CELL_SIZE = WIDTH // 3
OFFSET = 10
FONT_SIZE = 30

SNAKE_CELL = 20
SNAKE_SPEED = 10


def main():
    # INITIALIZE PYGAME
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

    pygame.quit()


class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = SNAKE_SPEED
        self.direction = "RIGHT"
        self.font = pygame.font.SysFont("consolas", FONT_SIZE)
        self.running = True
        self.score = 0
        self.gameIsOver = False

        self.snake = []
        self.snakeLength = 1
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.dx = 0
        self.dy = 0
        
        # Food at Random position on the screen
        self.foodX = int(random.randrange(1, WIDTH//SNAKE_CELL) * SNAKE_CELL)
        self.foodY = int(random.randrange(1, HEIGHT//SNAKE_CELL) * SNAKE_CELL)

    def status(self, text, color):
        d = self.font.render(text, True, color)
        self.screen.blit(d, [WIDTH//12, HEIGHT // 2])

    def DrawSnake(self):
        for cell in self.snake:
            pygame.draw.rect(self.screen, GREEN, [
                             cell[0], cell[1], SNAKE_CELL, SNAKE_CELL])

    def Run(self):
        # Move offsets
        directions = {
            "RIGHT": [SNAKE_CELL, 0],
            "LEFT": [-SNAKE_CELL, 0],
            "UP": [0, -SNAKE_CELL],
            "DOWN": [0, SNAKE_CELL]
        }
        while self.running:
            self.HandleEvent()
            pygame.display.set_caption(f"SNAKE - score : {self.score}")

            if self.gameIsOver:
                self.status("Press 'Space' to restart or 'ESC' to quit", WHITE)
                pygame.display.flip()
            else:
                self.screen.fill(BLACK)

                self.dx = directions[self.direction][0]
                self.dy = directions[self.direction][1]

                # CHECK IF SNAKE IF OUT OF THE SCREEN - BOUNDARIES
                if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
                    self.gameIsOver = True
                
                # Apply offsets
                self.x += self.dx
                self.y += self.dy

                # Draw food rectangle
                pygame.draw.rect(self.screen, RED, [
                    self.foodX, self.foodY, SNAKE_CELL, SNAKE_CELL])

                # add snake head in snake list
                head = [self.x, self.y]
                self.snake.append(head)
                if len(self.snake) > self.snakeLength:
                    del self.snake[0]

                # Check If the Snake collided with itself
                for part in self.snake[:-1]:
                    if part == head:
                        self.gameIsOver = True

                self.DrawSnake()

                # Check if the snake ate the food
                # And put the food on another random position on the screen
                if self.x == self.foodX and self.y == self.foodY:
                    self.foodX = int(random.randrange(
                        1, WIDTH//SNAKE_CELL) * SNAKE_CELL)
                    self.foodY = int(random.randrange(
                        1, HEIGHT//SNAKE_CELL) * SNAKE_CELL)
                    self.snakeLength += 1
                    self.score += 1
                
                pygame.display.update()
                self.clock.tick(self.fps)

    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RIGHT:
                    if self.dx != -SNAKE_CELL:
                        self.direction = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    if self.dx != SNAKE_CELL:
                        self.direction = "LEFT"
                elif event.key == pygame.K_UP:
                    if self.dy != SNAKE_CELL:
                        self.direction = "UP"
                elif event.key == pygame.K_DOWN:
                    if self.dy != -SNAKE_CELL:
                        self.direction = "DOWN"
                elif event.key == pygame.K_SPACE:
                    # RESTART GAME
                    self.Reset()

    def Reset(self):
        self.gameIsOver = False
        self.foodX = int(random.randrange(1, WIDTH//SNAKE_CELL) * SNAKE_CELL)
        self.foodY = int(random.randrange(1, HEIGHT//SNAKE_CELL) * SNAKE_CELL)
        self.snakeLength = 1
        self.snake = []
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.score = 0
        self.dx = 0
        self.dy = 0

if __name__ == "__main__":
    main()
