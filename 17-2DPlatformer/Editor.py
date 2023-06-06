import pygame
from constants import *
from utils import RenderText, RenderGrid, RenderWorld
from components import Button
import pickle
import os

def main():
    # INITIALIZE PYGAME
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + 400, HEIGHT))
    pygame.display.set_caption("EDITOR")
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
        
        self.clicked = False
        self.selectedSprite = 1

        self.currentLevel = 1
        self.maxLevel = 20

        self.font = pygame.font.Font("./assets/fonts/dpcomic.ttf", 30)
        self.LoadSprites()
        self.LevelData = [[ 0 for j in range(WIDTH//TILESIZE)] for i in range(HEIGHT//TILESIZE)]
        
        self.background = pygame.image.load("./assets/images/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.LoadButton = Button(WIDTH+200, 100, self.loadButtonImage)
        self.SaveButton = Button(WIDTH+200, 300, self.saveButtonImage)


    def Run(self):
        while self.running:
            self.screen.fill((12, 12, 12))
            self.screen.blit(self.background, (0, 0))
            self.HandleEvent()

            if self.LoadButton.draw(self.screen):
                self.LoadLevel()
            elif self.SaveButton.draw(self.screen):
                self.SaveLevel()
            RenderText(self.screen, f"LEVEL {self.currentLevel}", self.font, WHITE, WIDTH + 200, 200)

            RenderWorld(self, self.screen)
            RenderGrid(self.screen, WIDTH//TILESIZE, TILESIZE)

            for index, button in enumerate(self.buttons):
                if button.draw(self.screen):
                    self.selectedSprite = index+1
                    print(index)
                if index == 10 :
                    RenderText(self.screen, "< >", self.font, WHITE, button.x ,button.y)
                elif index == 11:
                    RenderText(self.screen, "^", self.font, WHITE, button.x ,button.y)

            pygame.display.update()
    
    def LoadSprites(self):
        # LOAD ALL SPRITES OF THE LEVEL
        self.saveButtonImage = pygame.image.load("./assets/images/saveButton.png")
        self.loadButtonImage = pygame.image.load("./assets/images/loadButton.png")
        self.quitButtonImage = pygame.image.load("./assets/images/quitButton.png")
        
        self.saveButtonImage = pygame.transform.scale(self.saveButtonImage, (TILESIZE * 2, TILESIZE * 2))
        self.loadButtonImage = pygame.transform.scale(self.loadButtonImage, (TILESIZE * 2, TILESIZE * 2))
        self.quitButtonImage = pygame.transform.scale(self.quitButtonImage, (TILESIZE * 2, TILESIZE * 2))
        
        self.centerTileImage = pygame.image.load("./assets/images/centertile.png")
        self.coinImage = pygame.image.load("./assets/images/coin.png")
        self.leftTileImage = pygame.image.load("./assets/images/leftitle.png")
        self.rightTileImage = pygame.image.load("./assets/images/righttile.png")
        self.waterImage = pygame.image.load("./assets/images/water.png")
        self.platformImage = pygame.image.load("./assets/images/platform.png")
        self.snakeImage = pygame.image.load("./assets/images/snake1.png")
        self.tileImage = pygame.image.load("./assets/images/tile1.png")
        self.tileTopLeftImage = pygame.image.load("./assets/images/tilelefttop.png")
        self.tileTopRightImage = pygame.image.load("./assets/images/tilerighttop.png")
        self.playerImage = pygame.image.load("./assets/images/player0.png")
        self.portalImage = pygame.image.load("./assets/images/portal.png")

        self.buttons = []
        startX = WIDTH + TILESIZE
        startY = HEIGHT//2
        offset = 5
        # TILE SELECTOR BUTTONS
        # Lists of tiles by it ID
        tiles = [
            self.centerTileImage,
            self.tileImage,
            self.tileTopLeftImage,
            self.tileTopRightImage,
            self.rightTileImage,
            self.leftTileImage,
            self.snakeImage,
            self.waterImage,
            self.portalImage,
            self.coinImage,
            self.platformImage,
            self.platformImage
        ]
        TileSizeEditor = TILESIZE + 10
        num_rows = 5
        row_counter = 0
        for index, tile in enumerate(tiles):
            scaledImage = pygame.transform.scale(tile, (TileSizeEditor - offset, TileSizeEditor - offset))
            if (index % num_rows) == 0:
                row_counter += 1
            button = Button(
            startX + index % num_rows * TileSizeEditor, 
            startY + row_counter * TileSizeEditor, 
            scaledImage
            )
            
            self.buttons.append(button)
    
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    self.currentLevel = (self.currentLevel + 1) % self.maxLevel
                elif event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                    if self.currentLevel == 0:
                        self.currentLevel = self.maxLevel
                    else:
                        self.currentLevel -= 1
        mouseX, mouseY = pygame.mouse.get_pos()
        # Get the translated position
        x = mouseX // TILESIZE
        y = mouseY // TILESIZE
        
        if x < WIDTH//TILESIZE:
            if pygame.mouse.get_pressed()[0] == 1:
                # print(f"coord: {x},{y}")
                self.LevelData[y][x] = self.selectedSprite
            elif pygame.mouse.get_pressed()[2] == 1:
                self.LevelData[y][x] = 0
    
    def LoadLevel(self):
        if os.path.exists(f"./data/LEVEL-{self.currentLevel}"):
            file = open(f"./data/LEVEL-{self.currentLevel}", 'rb')
            self.LevelData = pickle.load(file)
            print("Level loaded")
        else:
            print("Error, File doesn't exist")
    
    def SaveLevel(self):
        file = open(f"./data/LEVEL-{self.currentLevel}", "wb")
        pickle.dump(self.LevelData, file)
        file.close()
        print("level Saved")
        
                            
if __name__ == "__main__":
    main()