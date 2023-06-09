WIDTH = 1000
HEIGHT = 1000
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (80, 255, 100)
RED = (255, 120, 10)
FONT_SIZE = 25

TILESIZE = 50

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80

SNAKE_WIDTH = 40
SNAKE_HEIGHT = 40

SPEED = 8
JUMP_VEL = 16
MAX_LEVELS = 20

# ANIMATION SPEED
WALK_ANIMATION = 2
JUMP_ANIMATION = 4

SNAKE_ANIMATION = 3


TEST_LEVEL = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,10, 0, 0, 0, 0, 0, 2, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 2, 2, 2, 0, 0, 6,],
    [5, 0, 0,10, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 6,],
    [5, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 12, 0, 0, 6,],
    [5, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 2, 0, 0,10, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 6,],
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 7, 0, 0, 0, 0, 0, 6,],
    [1, 3, 2, 2, 2, 2, 8, 8, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 4, 1,]
]