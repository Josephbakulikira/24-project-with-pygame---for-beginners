import pygame
from constants import *
from utils import *
from board import Board
from position import Position
from tools import *
import time

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CHESS")
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

        self.currentTurn = 0
        self.gameOver = False
        self.board = Board()
        self.adjusted_mouse = Position(0, 0)

        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.selectedOrigin = None

        self.draggedPiece = None
        self.canBeReleased = False


        self.font = pygame.font.SysFont("consolas", 18, bold=True)
    
    def Run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.screen.fill(BLACK)
            self.HandleEvent()
            self.GetMousePosition()

            self.Render()
            self.IsGameOver()
            pygame.display.update()
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonDown()
                elif event.button == 3:
                    pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.HandleOnLeftMouseButtonUp()
    
    def SelectPiece(self, piece):
        if piece != None and piece.color == self.board.player:
            self.selectedPiece = piece
            self.draggedPiece = piece
            self.selectedPieceMoves, self.selectedPieceCaptures = self.board.GetAllowedMoves(self.selectedPiece)
            self.selectedOrigin = piece.position.GetCopy()

    def ReleasePiece(self):
        self.selectedPiece = None
        self.selectedPieceMoves = None
        self.selectedPieceCaptures = None
        self.draggedPiece = None
        self.selectedOrigin = None
        
    def HandleOnLeftMouseButtonDown(self):
        if self.board.pieceToPromote != None and self.adjusted_mouse.x == self.board.pieceToPromote.position.x:
            choice = self.adjusted_mouse.y
            if choice <= 3 and self.board.player == 0:
                # Promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, choice)
                #Refresh screen
                self.Render()
            elif choice > 3 and self.board.player == 1:
                # promote pawn
                self.board.PromotePawn(self.board.pieceToPromote, 7-choice)
                # Refresh screen
                self.Render()
        else:
            if self.adjusted_mouse.OnBoard():
                piece = self.board.grid[self.adjusted_mouse.x][self.adjusted_mouse.y]
                if self.selectedPiece == piece:
                    self.draggedPiece = piece
                else:
                    self.SelectPiece(piece)
    def HandleOnLeftMouseButtonUp(self):
        self.draggedPiece = None
        if self.selectedPiece:
            if self.selectedOrigin != self.adjusted_mouse:
                if PositionIn(self.adjusted_mouse, self.selectedPieceCaptures):
                    self.board.Move(self.selectedPiece, self.adjusted_mouse)
                elif PositionIn(self.adjusted_mouse, self.selectedPieceMoves):
                    self.board.Move(self.selectedPiece, self.adjusted_mouse)
                self.ReleasePiece()
            elif self.canBeReleased:
                self.ReleasePiece()
            else:
                self.canBeReleased = True

             
    def Render(self):
        DrawChessBoard(self.screen)
        DrawChessCoordinates(self.screen, self.font)
        DrawPieces(self.screen, self.board)
        DrawHighlight(self.screen, self.board, self.selectedPiece, self.draggedPiece, self.selectedPieceMoves, self.selectedPieceCaptures, self.adjusted_mouse)
        self.RenderPromoteWindow()

    def GetMousePosition(self):
        x, y = pygame.mouse.get_pos()
        self.adjusted_mouse.x = (x - HORIZONTAL_OFFSET) // SQUARE_SIZE
        self.adjusted_mouse.y = (y - TOP_OFFSET//2) // SQUARE_SIZE
    
    def RenderPromoteWindow(self):
        if self.board.pieceToPromote:
            if self.board.pieceToPromote.color == 0:
                x = self.board.pieceToPromote.position.x * SQUARE_SIZE + HORIZONTAL_OFFSET
                y = self.board.pieceToPromote.position.y * SQUARE_SIZE + TOP_OFFSET // 2
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, SQUARE_SIZE , SQUARE_SIZE * 4])
                for i in range(4):
                    piece = self.board.whitePromotions[i]
                    self.screen.blit(piece.sprite, (x, i * SQUARE_SIZE + TOP_OFFSET //2 ))
                    bottomY = i * SQUARE_SIZE - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, SQUARE_SIZE , 2])
            else:
                x = self.board.pieceToPromote.position.x * SQUARE_SIZE + HORIZONTAL_OFFSET
                y = (self.board.pieceToPromote.position.y - 3) * SQUARE_SIZE + TOP_OFFSET // 2
                pygame.draw.rect(self.screen, (200, 200, 200), [x, y, SQUARE_SIZE , SQUARE_SIZE * 4])
                for i in range(4):
                    piece = self.board.blackPromotions[i]
                    self.screen.blit(piece.sprite, (x, (i+4) * SQUARE_SIZE + TOP_OFFSET //2 ))
                    bottomY = (i + 4) * SQUARE_SIZE - 1
                    pygame.draw.rect(self.screen, (0, 0, 0), [x, bottomY, SQUARE_SIZE , 2])
    
    def IsGameOver(self):
        if self.board.winner != None:
            self.gameOver = True
            self.GameOverQuit()
            
    def GameOverQuit(self):
        # if self.board.winner >= 0:
        #     # sounds.game_over_sound.play()
        #     print
        # else:
        #     sounds.stalemate_sound.play()
        print("GAME OVER")
        if self.board.winner == 0:
            print("White Win")
        elif self.board.winner == 1:
            print("black win")
        else:
            print("draw")
        time.sleep(2)
        self.running = False

if __name__ == "__main__":
    main()