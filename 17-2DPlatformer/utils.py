from constants import *
import pygame

def RenderText(screen, message, font, text_color=WHITE, x=WIDTH//2, y=HEIGHT//2):
    img = font.render(message, True, text_color)
    rect = img.get_rect()
    rect.center = (x, y)
    screen.blit(img, rect)

def RenderGrid(screen, rows, size):
    for i in range(rows):
        pygame.draw.line(screen, WHITE, (i * size, 0),(i * size, HEIGHT), 1)
        pygame.draw.line(screen, WHITE, (0, i * size),(WIDTH, i * size), 1)

def RenderWorld(game, screen):
    for v in range(WIDTH//TILESIZE):
        for w in range(HEIGHT//TILESIZE):
            if game.LevelData[v][w] == 1:
                sprite = pygame.transform.scale(game.centerTileImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 2:
                sprite = pygame.transform.scale(game.tileImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 3:
                sprite = pygame.transform.scale(game.tileTopLeftImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 4:
                sprite = pygame.transform.scale(game.tileTopRightImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 5:
                sprite = pygame.transform.scale(game.rightTileImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 6:
                sprite = pygame.transform.scale(game.leftTileImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 7:
                sprite = pygame.transform.scale(game.snakeImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 8:
                sprite = pygame.transform.scale(game.waterImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 9:
                sprite = pygame.transform.scale(game.portalImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 10:
                sprite = pygame.transform.scale(game.coinImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 11:
                sprite = pygame.transform.scale(game.platformImage, (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
            elif game.LevelData[v][w] == 12:
                sprite = pygame.transform.scale(game.platformImage , (TILESIZE, TILESIZE))
                screen.blit(sprite, (w*TILESIZE, v*TILESIZE))
