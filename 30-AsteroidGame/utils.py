import math
from vector import Vector
from constants import *
import pygame


def DrawTriangle(screen, position, front, backRight, backLeft, angle, size, color, show_direction):
    x, y = position.getTuple()
    angle = angle
    s = size

    pygame.draw.polygon(screen, color, [front.getTuple(), backRight.getTuple(), backLeft.getTuple()])

    if show_direction:
        ax = math.sin(angle) * 50 + x
        ay = -math.cos(angle) * 50 + y
        back = Vector.fromAngle(angle - math.pi, s//2) + position

        # DEBUG
        pygame.draw.circle(screen, color, (x, y), 2)
        pygame.draw.line(screen, RED, (x, y), (ax, ay), 1)
        pygame.draw.circle(screen, GREEN, front.getTuple(), 2)
        pygame.draw.circle(screen, (0, 0, 255), backRight.getTuple(), 2)
        pygame.draw.circle(screen, (255, 255, 0), backLeft.getTuple(), 2)
        pygame.draw.circle(screen, (255, 255, 0), back.getTuple(), 2)


def WrapDisplay(position, size):
    x, y = position.getTuple()
    if x + size > WIDTH:
        x = x - WIDTH
    elif x - size <= 0:
        x = x + WIDTH
    
    if y + size > HEIGHT:
        y = y - HEIGHT
    elif y - size <= 0:
        y = y + HEIGHT
    return x, y

def RenderText(screen, message, font, text_color=WHITE, x=WIDTH//2, y=HEIGHT//2):
    img = font.render(message, True, text_color)
    rect = img.get_rect()
    rect.center = (x, y)
    screen.blit(img, rect)

def IsPointInsideACirlce(point_position, circle_position, circle_radius, size=1):
    distance = Vector.GetDistance(point_position, circle_position)
    if distance - (size//1.3) <= circle_radius:
        return True
    else:
        return False

            
