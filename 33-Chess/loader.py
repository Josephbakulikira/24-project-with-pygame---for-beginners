import pygame
from constants import *

white_pawn = pygame.image.load("./assets/sprites/white_pawn.png")
white_bishop = pygame.image.load("./assets/sprites/white_bishop.png")
white_knight = pygame.image.load("./assets/sprites/white_knight.png")
white_rook = pygame.image.load("./assets/sprites/white_rook.png")
white_queen = pygame.image.load("./assets/sprites/white_queen.png")
white_king = pygame.image.load("./assets/sprites/white_king.png")

black_pawn = pygame.image.load("./assets/sprites/black_pawn.png")
black_bishop = pygame.image.load("./assets/sprites/black_bishop.png")
black_knight = pygame.image.load("./assets/sprites/black_knight.png")
black_rook = pygame.image.load("./assets/sprites/black_rook.png")
black_queen = pygame.image.load("./assets/sprites/black_queen.png")
black_king = pygame.image.load("./assets/sprites/black_king.png")

def GetSprite(piece):
    sprite = None
    if piece.code == 'p':
        if piece.color == 0:
            sprite = white_pawn
        else:
            sprite = black_pawn
    elif piece.code == 'b':
        if piece.color == 0:
            sprite = white_bishop
        else:
            sprite = black_bishop
    elif piece.code == 'n':
        if piece.color == 0:
            sprite = white_knight
        else:
            sprite = black_knight
    elif piece.code == 'r':
        if piece.color == 0:
            sprite = white_rook
        else:
            sprite = black_rook
    elif piece.code == 'q':
        if piece.color == 0:
            sprite = white_queen
        else:
            sprite = black_queen
    else:
        if piece.color == 0:
            sprite = white_king
        else:
            sprite = black_king
    transformed = pygame.transform.smoothscale(sprite, (SQUARE_SIZE, SQUARE_SIZE))
    return transformed