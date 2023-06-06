import pygame
import math
import random
from constants import *
from Vector import *
import colorsys

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

class Boid:
    def __init__(self, x, y, color=GREEN, radius=BOID_SIZE):
        self.position = Vector(x, y)
        self.color = color
        self.radius = radius
        self.angle = random.uniform(0, math.pi * 2)
        
        self.velocity = Vector(math.cos(self.angle), math.sin(self.angle))
        self.acceleration = Vector()

        self.max_speed = 2
        self.max_force = 0.04
    
    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.velocity.Limit(self.max_speed)
        self.position += self.velocity
        self.acceleration = Vector()
    
    def Boundary(self):
        if self.position.x < -self.radius: 
            self.position.x = WIDTH + self.radius
        if self.position.y < -self.radius:
            self.position.y = HEIGHT + self.radius
        if self.position.x > WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y > HEIGHT+self.radius:
            self.position.y = -self.radius
    
    def apply_force(self, force):
        self.acceleration += force
    
    def Seek(self, target):
        # Vector pointing from the position to the target
        desired = target - self.position

        desired = Vector.SetMagnitude(desired, self.max_speed)

        steer = desired - self.velocity
        steer = steer.Limit(self.max_force)

        return steer
    
    def align(self, boids):
        in_range = 50
        average = Vector()
        count = 0

        for other in boids:
            distance = Distance(self.position, other.position)
            if distance > 0 and distance < in_range:
                average += other.velocity
                count += 1
        
        if count > 0:
            average /= len(boids)
            average = Vector.SetMagnitude(average, self.max_speed)
            steer = average - self.velocity
            steer = steer.Limit(self.max_force)
            return steer
        else:
            return Vector()

    def separate(self, boids):
        desired = 25
        steer = Vector()
        count = 0
        
        for other in boids:
            distance = Distance(self.position, other.position)
            if distance > 0 and distance < desired:
                # Get The vector heading away from the other boids
                diff = self.position - other.position
                diff = Vector.Normalize(diff)
                diff /= distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        
        mag = Vector.Magnitude(steer)
        if mag > 0:
            steer = Vector.SetMagnitude(steer, self.max_speed)
            steer -= self.velocity
            steer = steer.Limit(self.max_force)
    
        return steer
    
    def cohesion(self, boids):
        in_range = 50
        average = Vector()
        count = 0

        for other in boids:
            distance = Distance(self.position, other.position)
            if distance > 0 and distance < in_range:
                average += other.position
                count += 1
        if count > 0:
            average /= count
            steer = self.Seek(average)
            return steer
        else:
            return Vector()

    def draw(self, screen):
        theta = Vector.Heading(self.velocity)

        top = Vector.fromAngle(theta, self.radius) + self.position
        backRight = Vector.fromAngle(theta - math.pi//2 - math.pi, self.radius//1.5) + self.position
        backLeft = Vector.fromAngle(theta + math.pi//2 - math.pi, self.radius//1.5) + self.position

        # self.color = hsv2rgb((self.position.x + self.position.y)/1000 , 1, 1)
        # pygame.draw.circle(screen, self.color, self.position.GetTuple(), self.radius)

        pygame.draw.polygon(screen, self.color, [top.GetTuple(), backRight.GetTuple(), backLeft.GetTuple()])
    
    def flock(self, boids):
        separate = self.separate(boids)
        align = self.align(boids)
        cohesion = self.cohesion(boids)

        separate *= SEPARATION
        align *= ALIGNMENT
        cohesion *= COHESION

        self.apply_force(separate)
        self.apply_force(align)
        self.apply_force(cohesion)

    
    def run(self, boids, screen):
        self.flock(boids)
        self.update()
        self.Boundary()
        self.draw(screen)