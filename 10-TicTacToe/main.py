import pygame

# CONSTANTS
WIDTH = 900
HEIGHT = 900
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (80, 255, 100)
CELL_SIZE = WIDTH // 3
OFFSET = 10
FONT_SIZE = 220
WINNER_FONT = 50

def main():
    # INITIALIZE PYGAME
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-tac-toe")
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

    pygame.quit()

class Game:
    def __init__(self, screen, clock):
        self.fps = 30
        self.screen = screen
        self.clock = clock
        self.running = True
        self.mouse_clicked = False
        self.font = pygame.font.SysFont("Consolas", FONT_SIZE)
        self.winnerFont = pygame.font.SysFont("Consolas", WINNER_FONT)
        self.winner = None
        self.player = 1
        self.gameIsOver = False
        self.boardIsFull = False
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.clock.tick(self.fps)

    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            
            self.HandleEvent()
            # -- GET MOUSE POSITION --
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x = mouse_x // CELL_SIZE
            mouse_y = mouse_y // CELL_SIZE

            # --- HANDLE ON MOUSE CLICKED ---
            if self.mouse_clicked and not self.gameIsOver:
                self.HandleClick(mouse_x, mouse_y)

            # --- DRAW BOARD ---
            for i in range(3):
                for j in range(3):
                    pos_x = i*CELL_SIZE + OFFSET//2
                    pos_y = j*CELL_SIZE + OFFSET//2
                    square = [pos_x, pos_y, CELL_SIZE - OFFSET, CELL_SIZE - OFFSET]
                    # hover color
                    color = GRAY if (mouse_x == i and mouse_y == j) else WHITE
                    pygame.draw.rect(self.screen, color, square)
                    
                    if self.board[i][j] != None:
                        text = "X" if self.board[i][j] == 1 else "O"
                        fontText = self.font.render(text, True, BLACK)
                        self.screen.blit(fontText, (pos_x + 80, pos_y+50))

            # RENDER WINNER TEXT
            if self.winner or self.boardIsFull == True:
                pygame.draw.rect(self.screen, GREEN, [0, HEIGHT//2 - 50, WIDTH, 100])
                text = "Player one Won the game" if self.winner == 1 else "Player two Won the game"
                if self.boardIsFull == True:
                    text = "Draw, Restart the game"
                fontText = self.winnerFont.render(text, True, BLACK)
                self.screen.blit(fontText, (180, HEIGHT//2 - 25))
            

            pygame.display.update()
            self.mouse_clicked = False
    
    def HandleClick(self, x, y):
        if self.board[x][y] == None:
            self.board[x][y] = self.player
        self.Check()
        if not self.winner and self.boardIsFull == False:
            self.SwitchPlayerTurn()
        
    
    def SwitchPlayerTurn(self):
        self.player = 1 if self.player == 2 else 2
    
    def Check(self):
        # CHECK IF THE GAME IS OVER
        if not self.gameIsOver:
            if self.board[0][0] == self.board[0][1] and self.board[0][1] == self.board[0][2] and self.board[0][0] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[1][0] == self.board[1][1] and self.board[1][1] == self.board[1][2] and self.board[1][0] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[2][0] == self.board[2][1] and self.board[2][1] == self.board[2][2] and self.board[2][0] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[0][0] == self.board[1][0] and self.board[1][0] == self.board[2][0] and self.board[0][0] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[0][1] == self.board[1][1] and self.board[1][1] == self.board[2][1] and self.board[0][1] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[0][2] == self.board[1][2] and self.board[1][2] == self.board[2][2] and self.board[0][2] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True
            elif self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0] and self.board[0][2] != None:
                self.winner = self.player
                print(f"WINNER IS -> {self.player} ")
                self.gameIsOver = True

            self.boardIsFull = True
            self.gameIsOver = True
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == None:
                        self.boardIsFull = False
                        self.gameIsOver = False

    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    # RESTART GAME
                    self.winner = None
                    self.board = [
                        [None, None, None],
                        [None, None, None],
                        [None, None, None]
                    ]
                    self.boardIsFull = False
                    self.player = 1
                    self.gameIsOver = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_clicked = True


if __name__ == "__main__":
    main()
