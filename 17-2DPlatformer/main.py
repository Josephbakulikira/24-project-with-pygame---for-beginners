import pygame
from constants import *
from components import *
from utils import RenderText
import os
import pickle

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D - PLATFORMER")
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

        # GAME VARIABLES
        self.gameOver = 0
        self.currentLevel = 1
        self.score = 0
        self.mainMenu = True

        self.scoreFont = pygame.font.Font("./assets/fonts/dpcomic.ttf", 35)
        self.font = pygame.font.Font("./assets/fonts/dpcomic.ttf", 80)

        # SPRITE GROUPS
        self.snakes = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectables = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        coin_icon = Coin(TILESIZE//2, TILESIZE//2)
        self.collectables.add(coin_icon)
        # load images
        self.background = pygame.image.load("./assets/images/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.restartButtonImage = pygame.image.load("./assets/images/restartButton.png")
        self.restartButtonImage = pygame.transform.scale(self.restartButtonImage, (100, 100))

        self.quitButtonImage = pygame.image.load("./assets/images/quitButton.png")
        self.quitButtonImage = pygame.transform.scale(self.quitButtonImage, (100, 100))

        self.startButtonImage = pygame.image.load("./assets/images/playButton.png")
        self.startButtonImage = pygame.transform.scale(self.startButtonImage, (100, 100))

        # load sounds
        pygame.mixer.music.load("./assets/audio/backgroundmusic.wav")
        pygame.mixer.music.play(-1, 0.0, 5000)
        
        self.coinFX = pygame.mixer.Sound("./assets/audio/coin.wav")
        self.coinFX.set_volume(0.4)
        

        #Load Level and Initialize world
        if os.path.exists(f"./data/LEVEL-{self.currentLevel}"):
            file = open(f"./data/LEVEL-{self.currentLevel}", "rb")
            data = pickle.load(file)
            self.world = World(self.snakes, self.collectables, self.platforms, self.waters, self.portals, data)
        else:
            print("ERROR LOADING THE LEVEL, CHECK IF YOU HAVE ALL THE REQUIRED FILES")
            self.world = World(self.snakes, self.collectables, self.platforms, self.waters, self.portals)
        
        self.player = Player(TILESIZE+20, HEIGHT - TILESIZE - PLAYER_HEIGHT)

        self.restartButton = Button(WIDTH//2, HEIGHT//2 + 200, self.restartButtonImage)
        self.startButton = Button(WIDTH//2 - 100, HEIGHT//2, self.startButtonImage)
        self.quitButton = Button(WIDTH//2 + 100, HEIGHT//2, self.quitButtonImage)

    def Run(self):
        while self.running:
            # Set frame rate
            self.clock.tick(self.fps)
            self.SetCaption(int(self.clock.get_fps()))
            self.HandleEvent()

            # DRAW BACKGROUND
            self.screen.fill(BLACK)

            self.screen.blit(self.background, (0, 0))
            if self.mainMenu:
                if self.startButton.draw(self.screen):
                    self.mainMenu = False
                if self.quitButton.draw(self.screen):
                    self.running = False
            else:
                if self.gameOver == 0:
                    # GAME LOOP
                    self.gameOver = self.player.Update(self.world.tiles, self.gameOver, self.world)
                    self.snakes.update(self.screen)
                    self.platforms.update(self.screen)
    
                # Render
                self.world.Render(self.screen)

                # GROUPS
                self.collectables.draw(self.screen)
                self.waters.draw(self.screen)
                self.platforms.draw(self.screen)
                self.portals.draw(self.screen)
                self.collectables.draw(self.screen)
                self.snakes.draw(self.screen)
                
                # COLLECT COINS
                if pygame.sprite.spritecollide(self.player, self.collectables, True):
                    self.score += 1
                    self.coinFX.play()
                self.player.Render(self.screen)

                if self.gameOver == -1:
                    # GAME OVER
                    RenderText(self.screen, "GAME OVER", self.font)
                    if self.restartButton.draw(self.screen):
                        self.Restart()
                if self.gameOver == 1:
                    # LEVEL COMPLETED
                    RenderText(self.screen, "LEVEL COMPLETED", self.font)
                    self.currentLevel += 1
                    if self.currentLevel <= MAX_LEVELS:
                        # RESET LEVES
                        self.player.Initialize(TILESIZE+20, HEIGHT - TILESIZE - PLAYER_HEIGHT)
                        self.LoadNextLevel(self.currentLevel)
                        self.gameOver = 0


                # DISPLAY SCORE
                RenderText(self.screen, f"  x {self.score}", self.scoreFont, WHITE, TILESIZE, TILESIZE//2)

            pygame.display.update()
        
    def HandleEvent(self):
        # Handle user Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def LoadNextLevel(self, new_level):
        self.collectables.empty()
        self.waters.empty()
        self.platforms.empty()
        self.portals.empty()
        self.collectables.empty()
        self.snakes.empty()
        # Load in level data and create world
        if os.path.exists(f"./data/LEVEL-{new_level}"):
            file = open(f"./data/LEVEL-{new_level}", "rb")
            data = pickle.load(file)
            self.world = World(self.snakes, self.collectables, self.platforms, self.waters, self.portals, data)
        else:
            print(f"LEVEL {new_level} not found")
    def SetCaption(self, frame_rate):
        # Set Frame rate of the screen
        pygame.display.set_caption(f"FPS: {frame_rate}")
    
    def Restart(self):
        self.player.Initialize(TILESIZE+20, HEIGHT - TILESIZE - PLAYER_HEIGHT)
        self.gameOver = 0

if __name__ == "__main__":
    main()