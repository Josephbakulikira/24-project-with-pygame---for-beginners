import pygame
from constants import *
import random

class Bird(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frames_length = 3
        self.import_frames()
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.JumpSound = pygame.mixer.Sound("./assets/audio/WING.mp3")
        self.JumpSound.set_volume(0.5)
        self.rect = self.image.get_rect(midleft=(WIDTH//20, HEIGHT//2))
        self.position = pygame.math.Vector2(self.rect.topleft)

        self.gravity = 650
        self.direction = 0

    
    def import_frames(self):
        self.frames = []
        for i in range(self.frames_length):
            sprite = pygame.image.load(f"./assets/sprites/blue-{i+1}.png").convert_alpha()
            scale = pygame.math.Vector2(sprite.get_size()) * 1.8
            scaled_image = pygame.transform.scale(sprite, (round(scale.x), round(scale.y)))
            self.frames.append(scaled_image)
    
    def update(self, dt):
        self.Fall(dt)
        self.Animate(dt)
        self.Rotate()
    
    def Fall(self, dt):
        self.direction += self.gravity * dt
        self.position.y += self.direction * dt
        self.rect.y = round(self.position.y)
    
    def Jump(self):
        self.direction = -320
        self.JumpSound.play()
    
    def Animate(self, dt):
        self.frame_index += 13 * dt
        self.image = self.frames[int(self.frame_index)%self.frames_length]
    
    def Rotate(self):
        rotated_bird = pygame.transform.rotozoom(self.image, self.direction * 0.07 * -1, 1)
        self.image = rotated_bird

class Pipe(pygame.sprite.Sprite):
    def __init__(self, groups, orientation, x, y):
        super().__init__(groups)
        self.type = "OBSTACLE"

        sprite = pygame.image.load('./assets/sprites/pipe-green.png')
        scale = pygame.math.Vector2(sprite.get_size()) 
        factor = HEIGHT // scale.y
        self.image = pygame.transform.scale(sprite, (round(scale.x * 1.8 ) , round(scale.y * factor) ))
        self.killSound = pygame.mixer.Sound('./assets/audio/POINT.mp3')
        self.killSound.set_volume(0.2)
        if orientation == "DOWN":
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midbottom=(x, y))
        self.position = pygame.math.Vector2(self.rect.topleft)

        
    
    def update(self, dt):
        self.position.x -= 400 * dt
        self.rect.x = round(self.position.x)
        if self.rect.right <= 50:
            self.kill()
            self.killSound.play()

class Background(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        sprite = pygame.image.load('./assets/sprites/background-day.png').convert()
        background = pygame.transform.scale(sprite, (WIDTH, HEIGHT))
        self.image = pygame.Surface((WIDTH * 2, HEIGHT))
        self.image.blit(background, (0, 0))
        self.image.blit(background, (WIDTH, 0))


        self.rect = self.image.get_rect(topleft=(0, 0))
        self.position = pygame.math.Vector2(self.rect.topleft)
    
    def update(self, dt):
        self.position.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.position.x = 0
        self.rect.x = round(self.position.x)

class Ground(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.type = "GROUND"

        sprite = pygame.image.load('./assets/sprites/base.png').convert_alpha()
        scale = pygame.math.Vector2(sprite.get_size())
        factor = WIDTH / scale.x
        self.image = pygame.transform.scale(sprite, (round(scale.x * factor) * 2, 100))

        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))
        self.position = pygame.math.Vector2(self.rect.topleft)
    
    def update(self, dt):
        self.position.x -= 350 * dt
        if self.rect.centerx <= 0:
            self.position.x = 0
        self.rect.x = round(self.position.x)