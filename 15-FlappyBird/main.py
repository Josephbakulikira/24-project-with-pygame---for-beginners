import pygame
from constants import *
from utils import *
import time
import random

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    # Set Window icon
    pygame.display.set_icon(pygame.image.load('./assets/favicon.ico'))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    game = Game(screen, clock)
    # Game Mainloop
    game.Run()

    pygame.quit()

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fps = 60
        self.running = True
        self.font = pygame.font.Font("./assets/font/04B_30__.TTF", FONT_SIZE)
        self.fontGameOver = pygame.font.Font("./assets/font/04B_30__.TTF", FONT_SIZE * 2)
        
        self.DieSound = pygame.mixer.Sound("./assets/audio/DIE.mp3")
        self.DieSound.set_volume(0.6)
        self.HitSound = pygame.mixer.Sound("./assets/audio/HIT.mp3")
        self.HitSound.set_volume(0.6)
        self.StartSound = pygame.mixer.Sound("./assets/audio/SWOOSH.mp3")
        self.StartSound.set_volume(0.3)

        self.score = 0
        self.sprites = pygame.sprite.Group()
        self.collisionSprites = pygame.sprite.Group()
        
        # sprites setup
        Background(self.sprites)
        Ground([self.sprites, self.collisionSprites])
        self.player = Bird(self.sprites)
        
        self.alive = True
        self.startOffset = 0

        self.pipe_spawn_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.pipe_spawn_timer, 1400)

        surf = pygame.image.load("./assets/sprites/message.png").convert_alpha()
        scale = pygame.math.Vector2(surf.get_size()) * 1.8
        self.message_surf = pygame.transform.scale(surf, (round(scale.x ) , round(scale.y) ))
        self.message_rect= self.message_surf.get_rect(center = (WIDTH//2, HEIGHT//2))

    def collisions(self):
        if pygame.sprite.spritecollide(self.player, self.collisionSprites, False):
            self.alive = False
            self.player.kill()
            self.HitSound.play()
            self.DieSound.play()
            for s in self.collisionSprites:
                if s.type == "OBSTACLE":
                    s.kill()
                    

    def RenderScore(self):
        if self.alive:
            self.score = (pygame.time.get_ticks() - self.startOffset) // 1000
            score_surf = self.font.render(str(self.score), True, WHITE)
        else:
            score_surf = self.fontGameOver.render(str(self.score), True, BLACK)
        score_rect = score_surf.get_rect(midtop = (WIDTH//2, HEIGHT//10))
        self.screen.blit(score_surf, score_rect)

    def Run(self):
        t = time.time()
        while self.running:
            self.HandleEvent()

            # delta time
            dt = time.time() - t
            t = time.time()
            
            self.sprites.update(dt)
            self.sprites.draw(self.screen)
            self.RenderScore()

            if self.alive: 
                self.collisions()
            else:
                self.screen.blit(self.message_surf, self.message_rect)

            pygame.display.update()
            self.clock.tick(self.fps)
        
    def HandleEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    if self.alive:
                        self.player.Jump()
                    else:
                        self.player = Bird(self.sprites)
                        self.alive = True
                        self.startOffset = pygame.time.get_ticks()
                        self.StartSound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 :
                    if self.alive:
                        self.player.Jump()
                    else:
                        self.player = Bird(self.sprites)
                        self.alive = True
                        self.startOffset = pygame.time.get_ticks()
                        self.StartSound.play()
            if event.type == self.pipe_spawn_timer and self.alive:
                x = WIDTH + random.randint(40, 100)
                y1 = random.randint(40, HEIGHT-320)
                y2 = HEIGHT - y1 * -1
                Pipe([self.sprites, self.collisionSprites], "UP", x, y1)
                Pipe([self.sprites, self.collisionSprites], "DOWN", x, y2)



if __name__ == "__main__":
    main()