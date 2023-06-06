import pygame
pygame.mixer.init()
WIDTH = 1920
HEIGHT = 1080
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)

FONT_SIZE = 25

BOARD_SIZE = 8
TOP_OFFSET = 20

SQUARE_SIZE = (HEIGHT - TOP_OFFSET) // BOARD_SIZE
HORIZONTAL_OFFSET = WIDTH // 2 - (SQUARE_SIZE * (BOARD_SIZE//2))

HIGHLIGHT_OUTLINE = 5

DARK = (112, 102, 119)
LIGHT = (204, 183, 174)

class Sound:
    def __init__(self):
        self.capture_sound = pygame.mixer.Sound("./assets/audio/capture_sound.mp3")
        self.castle_sound = pygame.mixer.Sound("./assets/audio/castle_sound.mp3")
        self.check_sound = pygame.mixer.Sound("./assets/audio/check_sound.mp3")
        self.checkmate_sound = pygame.mixer.Sound("./assets/audio/checkmate_sound.mp3")
        self.game_over_sound = pygame.mixer.Sound("./assets/audio/gameover_sound.mp3")
        self.game_start_sound = pygame.mixer.Sound("./assets/audio/start_sound.mp3")
        self.move_sound = pygame.mixer.Sound("./assets/audio/move_sound.mp3")
        self.stalemate_sound = pygame.mixer.Sound("./assets/audio/stalemate_sound.mp3")
        self.pop = pygame.mixer.Sound("./assets/audio/pop.mp3")

sounds = Sound()