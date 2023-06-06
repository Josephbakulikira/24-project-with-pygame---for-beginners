import pygame
from pygame import mixer
from constants import *
import random
import math

mixer.init()

def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2) * ( (value - min1) / (max1 - min1))

class Ball:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.radius = 20
        self.color = WHITE
        self.theta = random.uniform(-math.pi/3, math.pi/3)
        self.velX = BALL_SPEED * math.cos(self.theta)
        self.velY = BALL_SPEED * math.sin(self.theta)
        self.hitSound = mixer.Sound("./assets/hit.mp3")
        self.hitSound.set_volume(0.2)
        self.scoreSound = mixer.Sound("./assets/score.mp3")
        self.scoreSound.set_volume(0.1)

    def update(self):
        self.x += self.velX
        self.y += self.velY
            

    def Hit(self, paddle, left=True):
        if left:
            if self.y < paddle.y + paddle.height//2 and \
                self.y > paddle.y - paddle.height//2 and \
                self.x - self.radius < paddle.x + paddle.width//2:
                if self.x > paddle.x:
                    d = self.y - (paddle.y - paddle.height//2)
                    self.theta = translate(d, 0, paddle.height, -math.radians(45), math.radians(45))
                    
                    self.velX = BALL_SPEED * math.cos(self.theta)
                    self.velY = BALL_SPEED * math.sin(self.theta)
                    self.x = paddle.x + self.radius + paddle.width//2
                    self.hitSound.play()
        else:   
            if self.y < paddle.y + paddle.height//2 and \
                self.y > paddle.y - paddle.height//2 and \
                self.x + self.radius > paddle.x - paddle.width//2:
                if self.x < paddle.x:
                    d = self.y - (paddle.y - paddle.height//2)
                    self.theta = translate(d, 0, paddle.height, math.radians(225), math.radians(135))
                    
                    self.velX = BALL_SPEED * math.cos(self.theta)
                    self.velY = BALL_SPEED * math.sin(self.theta)
                    self.x = paddle.x - self.radius - paddle.width//2
                    self.hitSound.play()
                    

    def Boundary(self, left_score, right_score):
        if (self.y - self.radius) <= 0 or (self.y + self.radius) >= HEIGHT:
            self.velY *= -1

        if (self.x - self.radius) <= 0:
            self.Reset()
            right_score += 1
            self.scoreSound.play()

        elif (self.x + self.radius) >= WIDTH:
            self.Reset()
            left_score += 1
            self.scoreSound.play()


        return left_score, right_score

    def Reset(self):
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.theta = random.uniform(-math.pi/3, math.pi/3)

        self.velX = BALL_SPEED * math.cos(self.theta)
        self.velY = BALL_SPEED * math.sin(self.theta)

        if random.random() > 0.5:
            self.velX *= -1

    def Draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
