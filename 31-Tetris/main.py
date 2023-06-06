import pygame
from utils import *
from constants import *
import time

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TETRIS GAME")
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
        self.font = pygame.font.Font("./font/04B_30__.TTF", 50)

        self.gameOver = False

        pick = random.randint(0, 6)
        self.current_piece = pick
        self.current_rotation = 0
        self.current_x = W//2
        self.current_y = 0
        self.grid = []
        self.xCounter = XCOUNTER

        self.speed = SPEED
        self.accelerationFactor = 7
        self.debug = False

        self.score = 0

        for i in range(H):
            row = []
            for j in range(W):
                if j == 0 or j == (W-1) or i == (H-1):
                    row.append(1)
                else:
                    row.append(0)
            self.grid.append(row)
        self.completedLines = []
        
    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            dt = self.clock.tick(self.fps)/1000
            
            self.HandleEvent(dt)

            DrawGrid(self.screen, self.grid)
            if not self.gameOver:
                # draw the current piece
                DrawCurrentPiece(
                    self.screen, self.current_piece, int(self.current_x), 
                    int(self.current_y), self.current_rotation)
                if self.debug:
                    if DoesPieceFit(self.grid, self.current_piece, self.current_rotation, int(self.current_x), int(self.current_y)+1, self.screen, COLORS[self.current_piece+2]):
                        pass
                if int(self.current_y) < H-2 and DoesPieceFit(self.grid, self.current_piece, self.current_rotation, int(self.current_x), int(self.current_y)+1):
                    self.current_y += 1 * dt * self.speed
                else:
                    # Add the piece in the grid
                    LockPieceIntoGrid(self.grid, self.current_piece, int(self.current_x), int(self.current_y), self.current_rotation)
                    # Check if there is a complete horizontal line
                    CheckForRows(self.grid, self.completedLines, int(self.current_y))
                    DrawGrid(self.screen, self.grid)

                    # pick and set a random piece as the current piece
                    pick = random.randint(0, 6)
                    self.current_piece = pick
                    self.current_x = W//2
                    self.current_y = 0
                    self.current_rotation = 0
                    # Piece doest not fit
                    if not DoesPieceFit(self.grid, self.current_piece, self.current_rotation, int(self.current_x), int(self.current_y)):
                        self.gameOver = True

            # Draw grid lines
            DrawGridLines(self.screen)

            if self.gameOver:
                RenderText(self.screen, "GAME OVER", self.font, WHITE, WIDTH//2, HEIGHT//1.5)
                RenderText(self.screen, "Score: " + str(self.score), self.font, WHITE, WIDTH//2, HEIGHT//2)
            
            pygame.display.update()
            if len(self.completedLines) > 0:
                self.score += len(self.completedLines)
                # Show some delays
                time.sleep(0.3)
                for line in self.completedLines:
                    for x in range(1, W-1):
                        for y in range(line, 0, -1):
                            self.grid[y][x] = self.grid[y-1][x]
                        # self.grid[x][y] = 0
                self.completedLines.clear()
        
    def HandleEvent(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # TOGGLE DEBUG MODE
                    self.debug = not self.debug
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if DoesPieceFit(self.grid, self.current_piece, (self.current_rotation + 1) % 4, int(self.current_x), int(self.current_y)):
                        self.current_rotation = (self.current_rotation + 1) % 4

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if DoesPieceFit(self.grid, self.current_piece, self.current_rotation, int(self.current_x)+1, int(self.current_y), self.screen):
                if self.xCounter == XCOUNTER:
                    self.current_x += 1
                    self.xCounter = 0
                self.xCounter += 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if DoesPieceFit(self.grid, self.current_piece, self.current_rotation, int(self.current_x)-1, int(self.current_y), self.screen):
                if self.xCounter == XCOUNTER:
                    self.current_x -= 1
                    self.xCounter = 0
                self.xCounter += 1
        else:
            self.xCounter = XCOUNTER
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed = SPEED * self.accelerationFactor
        else:
            self.speed = SPEED

    
if __name__ == "__main__":
    main()