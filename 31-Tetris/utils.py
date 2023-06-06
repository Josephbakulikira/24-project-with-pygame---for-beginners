import random
import pygame
import math
from constants import *
from tetrimino import tetriminoes

def DrawGrid(screen, grid):
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            field = grid[x][y]
            color = COLORS[field]
            pygame.draw.rect(screen, color, [y * BOX_SIZE, x * BOX_SIZE, BOX_SIZE, BOX_SIZE])

        
def DrawGridLines(screen):
    # HORIZONTAL LINES
        for i in range(W):
            x = i * BOX_SIZE
            d = x + HEIGHT
            pygame.draw.line(screen, GRID_LINES, (x, 0), (x, d), 1)
        # VERTICAL LINES
        for i in range(H):
            y = i * BOX_SIZE
            d = y + WIDTH
            pygame.draw.line(screen, GRID_LINES, (0, y), (d, y), 1)
            
def DrawCurrentPiece(screen, piece, x, y, rotation):
    for i in range(4):
        for j in range(4):
            current_piece = tetriminoes[piece]
            transformed_index = RotateTetrimino(i, j, rotation)
            value = current_piece[transformed_index]
            if value > 1:
                v = (x + i - 2) * BOX_SIZE
                w = (y + j - 2) * BOX_SIZE
                pygame.draw.rect(screen, COLORS[value], [v, w, BOX_SIZE, BOX_SIZE])

def RotateTetrimino(x, y, rotation_value):
    if rotation_value == 0:
        # in case of 0 degree
        return y * 4 + x
    elif rotation_value == 1:
        # in case of 90 degree
        return 12 + y - (x * 4)
    elif rotation_value == 2:
        # in case of 180 degree
        return 15 - (y * 4) - x
    elif rotation_value == 3:
        # in case of 270 degree
        return 3 - y + (x * 4)
    else:
        return None

def DoesPieceFit(grid, tetrimino_index, rotation_val, dx, dy, screen=None, color=None):
    for x in range(4):
        for y in range(4):
            # Get index in tetrimino piece
            flat_index = RotateTetrimino(x, y, rotation_val)
            
            pos_x = dx + x - 2
            pos_y = dy + y - 2

            # Check if grid index is in range
            if pos_x >= 0 and pos_x < W:
                if pos_y >= 0 and pos_y < H:
                    if screen and color:
                            # DEBUG
                            pygame.draw.circle(screen, color,  (pos_x * BOX_SIZE, pos_y * BOX_SIZE), 5)
                            # print(f"position -> {pos_x}, {pos_y}")
                            # print(f"size: {len(grid)}, {len(grid[0])}")
                            # print(f"tetramino_index: {tetrimino_index}")
                            # print(f"index: {tetrimino_index}")
                    if tetriminoes[tetrimino_index][flat_index] > 1 and grid[pos_y][pos_x] != 0:
                        return False
    return True

def CheckForRows(grid, lines_list, y):
    for i in range(4):
        if (y + 1)-2 < H-1:
            row_completed = True
            for j in range(1, W-1):
                newY = y+i-2
                if grid[newY][j] <= 1:
                    row_completed = False
            if row_completed:
                # print("completed")
                for j in range(1, W-1):
                    newY = y+i-2
                    grid[newY][j] = 9
                lines_list.append(newY)
                    
def LockPieceIntoGrid(grid, piece_index, pieceX, pieceY, rotation):
    for x in range(4):
        for y in range(4):
            flat_index = RotateTetrimino(x, y, rotation)
            piece = tetriminoes[piece_index]
            if piece[flat_index] > 1:
                newX = pieceX + x - 2
                newY = pieceY + y - 2
                grid[newY][newX] = piece[flat_index]

def RenderText(screen, message, font, text_color=WHITE, x=WIDTH//2, y=HEIGHT//2):
    img = font.render(message, True, text_color)
    rect = img.get_rect()
    rect.center = (x, y)
    screen.blit(img, rect)