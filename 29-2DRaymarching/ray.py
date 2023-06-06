import pygame
from constants import *
from math import cos, sin
from utils import *

class Ray:
    def __init__(self, x, y, angle, color):
        self.position = [x, y]
        self.angle = angle
        self.color = color

        self.x_pos = 0
        self.y_pos = 0
        self.collsions = []
    
    def March(self, obstacles, collisions, screen):
        counter = 0
        current_pos = self.position
        # Draw origin
        pygame.draw.circle(screen, ORANGE, self.position, 5)

        while counter < 100:
            record = 2000
            closest = None
            for obstacle in obstacles:
                distance = SignedDistance(current_pos, obstacle, obstacle.radius)
                if distance < record:
                    record = distance
                    closest = obstacle
            
            if record < 1:
                collisions.insert(0, (int(current_pos[0]), int(current_pos[1])) )
                break

            self.x_position = current_pos[0] + cos(self.angle) * record
            self.y_position = current_pos[1] + sin(self.angle) * record

            aX = current_pos[0] + cos(self.angle) * record
            aY = current_pos[1] + sin(self.angle) * record

            pygame.draw.circle(screen, GREEN, (int(current_pos[0]), int(current_pos[1])), abs(int(record)), 1)
            pygame.draw.line(screen, self.color, (self.position[0], self.position[1]), (aX, aY), 4)

            current_pos[0] =  aX
            current_pos[1] =  aY

            pygame.draw.circle(screen, self.color, (int(self.x_pos), int(self.y_pos)), 4)

            closest.draw(screen, LIGHT_ORANGE)

            if offScreen([self.x_pos, self.y_pos], WIDTH, HEIGHT):
                break
            if offScreen(current_pos, WIDTH, HEIGHT):
                break
            
            counter += 1

