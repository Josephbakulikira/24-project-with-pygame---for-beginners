import pygame
from constants import *

def DrawChessBoard(screen):
    # drawing the empty chess board
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x = i * SQUARE_SIZE + HORIZONTAL_OFFSET
            y = j * SQUARE_SIZE + TOP_OFFSET//2

            if (i+j)%2 == 0:
                pygame.draw.rect(screen, LIGHT, [x, y, SQUARE_SIZE, SQUARE_SIZE])
            else:
                pygame.draw.rect(screen, DARK, [x, y, SQUARE_SIZE, SQUARE_SIZE])

def DrawChessCoordinates(screen, font):
    # Drawing chess coordinates (ranks, files)
    for i in range(BOARD_SIZE):
        x = 0.05 * SQUARE_SIZE + HORIZONTAL_OFFSET
        y =  (0.05 + i) * SQUARE_SIZE + TOP_OFFSET 
        color = LIGHT
        if i%2 == 0:
            color = DARK

        font_render = font.render(str(8-i), True, color)
        screen.blit(font_render, (x, y))

        x =  (i + 0.9) * SQUARE_SIZE + HORIZONTAL_OFFSET 
        y = (BOARD_SIZE-1 + 0.75)  * SQUARE_SIZE + TOP_OFFSET
        color = DARK
        if i%2 == 0:
            color = LIGHT
        font_render = font.render(chr(ord("a") + i), True, color)
        screen.blit(font_render, (x, y))

def DrawPieces(screen, board):
    # Draw Previous position
    # Draw our pieces
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            newX = x * SQUARE_SIZE + HORIZONTAL_OFFSET
            newY = y * SQUARE_SIZE + TOP_OFFSET//2
            if board.grid[x][y] != None:
                screen.blit(board.grid[x][y].sprite, (newX, newY))

def DrawHighlight(screen, board, selectedPiece, draggedPiece, selectedPieceMoves, selectedPieceCaptures, adjustedMouse):
    # Highlight selected piece
    if selectedPiece:
        x = selectedPiece.position.x * SQUARE_SIZE + HORIZONTAL_OFFSET
        y = selectedPiece.position.y * SQUARE_SIZE + TOP_OFFSET//2
        pygame.draw.rect(screen, (190, 200, 222), [x, y, SQUARE_SIZE, SQUARE_SIZE])

        if draggedPiece == None:
            screen.blit(selectedPiece.sprite, (x, y))
        
    # Draw selected piece possible moves
    if selectedPiece and selectedPieceMoves:
        for move in selectedPieceMoves:
            x = move.x * SQUARE_SIZE + HORIZONTAL_OFFSET
            y = move.y * SQUARE_SIZE + TOP_OFFSET//2

            pygame.draw.rect(screen, (40, 130, 210), [x, y, SQUARE_SIZE, SQUARE_SIZE], HIGHLIGHT_OUTLINE)
    # Draw selected piece captures
    if selectedPiece and selectedPieceMoves:
        for move in selectedPieceCaptures:
            x = move.x * SQUARE_SIZE + HORIZONTAL_OFFSET
            y = move.y * SQUARE_SIZE + TOP_OFFSET//2

            pygame.draw.rect(screen, (40, 230, 110), [x, y, SQUARE_SIZE, SQUARE_SIZE], HIGHLIGHT_OUTLINE)
    # Draw Dragged piece
    if draggedPiece:
        x = adjustedMouse.x * SQUARE_SIZE + HORIZONTAL_OFFSET
        y = adjustedMouse.y * SQUARE_SIZE + TOP_OFFSET//2
        screen.blit(draggedPiece.sprite, (x, y))
    
    # Highlight if in check
    # White king is in check
    if board.checkWhiteKing:
        x = board.WhiteKing.position.x * SQUARE_SIZE + HORIZONTAL_OFFSET
        y = board.WhiteKing.position.y * SQUARE_SIZE + TOP_OFFSET//2
        pygame.draw.rect(screen, (240, 111, 150), [x, y, SQUARE_SIZE, SQUARE_SIZE])
        screen.blit(board.WhiteKing.sprite, (x, y))
    # Black king is in check
    if board.checkBlackKing:
        x = board.BlackKing.position.x * SQUARE_SIZE + HORIZONTAL_OFFSET
        y = board.BlackKing.position.y * SQUARE_SIZE + TOP_OFFSET//2
        pygame.draw.rect(screen, (240, 111, 150), [x, y, SQUARE_SIZE, SQUARE_SIZE])
        screen.blit(board.BlackKing.sprite, (x, y))