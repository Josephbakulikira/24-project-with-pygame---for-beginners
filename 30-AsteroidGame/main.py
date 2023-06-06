import pygame
from constants import *
import random
from asteroid import Asteroid, AsteroidSpawner
from vector import Vector
from player import Player
from bullet import Bullet
from utils import *

def main():
    # INITIALIZE PYGAME
    pygame.init()
    # Pygame audio init
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ASTEROID GAME")
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

        self.score_font = pygame.font.Font("./assets/font/04B_30__.TTF", 30)
        self.font = pygame.font.Font("./assets/font/04B_30__.TTF", 70)
        
        self.player = Player(Vector(WIDTH//2, HEIGHT//2), 0)
        self.shoot = False

        self.asteroids = []
        self.bullets = []

        self.gameOver = False
        self.restart = False

        self.explosionFX = pygame.mixer.Sound("./assets/audio/explosion.wav")
        self.explosionFX.set_volume(0.5)
        self.deathFX = pygame.mixer.Sound("./assets/audio/death.wav")
        self.deathFX.set_volume(0.3)
        self.shootingFX = pygame.mixer.Sound('./assets/audio/shot.wav')
        self.shootingFX.set_volume(0.3)

        self.wave_timer = WAVE_TIMER

        AsteroidSpawner(self.asteroids, 5)

    def Run(self):
        while self.running:
            self.screen.fill(BLACK)
            dt = self.clock.tick(self.fps)/1000
            self.HandleEvent(dt)

            for asteroid in self.asteroids:
                if not self.gameOver:
                    asteroid.update(dt)
                    # CHECK COLLISION WITH PLAYER
                    if IsPointInsideACirlce(asteroid.position, self.player.position,  asteroid.size, self.player.size):
                        
                        self.gameOver = True
                        self.deathFX.play()
                        
                asteroid.draw(self.screen)

            for bullet in self.bullets:
                if not self.gameOver:
                    bullet.update(dt)
                    # CHECK COLLISION WITH ASTEROID
                    for asteroid in self.asteroids:
                        if IsPointInsideACirlce(bullet.position, asteroid.position, asteroid.size, bullet.size):
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            if asteroid in self.asteroids:
                                self.asteroids.remove(asteroid)
                            self.explosionFX.play()
                            if asteroid.size > MIN_ASTEROID_SPEED:
                                new_asteroid1 = Asteroid(asteroid.position + Vector.Random(-6, -3), asteroid.size//2)
                                new_asteroid2 = Asteroid(asteroid.position + Vector.Random(3, 6), asteroid.size//2)
                                self.asteroids.append(new_asteroid1)
                                self.asteroids.append(new_asteroid2)
                # DRAW
                bullet.draw(self.screen)
                if bullet.offScreen() and bullet in self.bullets:
                    self.bullets.remove(bullet)
                
            if self.gameOver:
                RenderText(self.screen, "GAME OVER", self.font, WHITE, WIDTH//2, HEIGHT//2)
            else:
                self.player.update(dt)

            self.player.draw(self.screen)
            pygame.display.update()
            self.wave_timer -= 1
            if self.wave_timer < 0:
                self.wave_timer = WAVE_TIMER
                AsteroidSpawner(self.asteroids, 3)

                        
        
    def HandleEvent(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_RETURN:
                    self.restart = True
                    self.asteroids = []
                    self.bullets = []
                    self.player = Player(Vector(WIDTH//2, HEIGHT//2), 0)
                    AsteroidSpawner(self.asteroids, 5)
                    self.gameOver = False
                    self.restar = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE :
                    bullet_velocity = Vector.fromAngle(self.player.angle) * BULLET_SPEED * dt
                    new_bullet = Bullet(self.player.position, bullet_velocity)
                    self.bullets.append(new_bullet)
                    self.shootingFX.play()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    bullet_velocity =  Vector.fromAngle(self.player.angle) * BULLET_SPEED * dt
                    new_bullet = Bullet(self.player.position, bullet_velocity)
                    self.bullets.append(new_bullet)
                    self.shootingFX.play()

                
if __name__ == "__main__":
    main()