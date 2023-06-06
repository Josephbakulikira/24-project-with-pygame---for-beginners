from constants import *
import pygame
from vector import Vector
from particle import Particle

class Polygon:
    def __init__(self, vertices, joints, static=[], line_thickness=4, color=WHITE):
        self.vertices = vertices
        self.joints = joints
        self.static = static

        self.distances = []
        for joint in joints:
            a = joint[0]
            b = joint[1]
            d = Vector.GetDistance(vertices[a].position, vertices[b].position)
            self.distances.append(d)

        self.color = color
        self.showPoint = True
        self.line_thickness = line_thickness
    
    def update(self, dt):
        for vertex in self.vertices:
            if not vertex in self.static:
                vertex.update(dt)
            if vertex.isClicked == True:
                mx, my = pygame.mouse.get_pos()
                vertex.position = Vector(mx, my)
            
    
    def constraint(self):
        for i in range(len(self.joints)):
            length = self.distances[i]
            a, b = self.joints[i]
            dist = Vector.GetDistance(self.vertices[a].position, self.vertices[b].position)
            diff_pos = self.vertices[a].position - self.vertices[b].position
            delta_length = length - dist

            current = diff_pos * 0.5 * delta_length / dist
            point_A = self.vertices[a]
            point_B = self.vertices[b]

            if (point_A in self.static or point_B in self.static) == False:
                point_A.position = point_A.position + current
                point_B.position = point_B.position - current
            if (point_A in self.static) == False and (point_B in self.static) == True:
                point_A.position = point_A.position + (current * 2)
            if (point_A in self.static) == True and (point_B in self.static) == False:
                point_B.position = point_B.position - (current * 2)


    def DeconnectOne(self, vertex):
        found = None
        for couple in self.joints:
            a, b = couple
            if self.vertices[a] == vertex or self.vertices[b] == vertex:
                found = couple
                break
        if found:
            self.joints.remove(found)


    def draw(self, screen):
        if len(self.vertices) < 2:
            print("The polygon class must have more than two particles")
            return

        for i in range(len(self.joints)):
            a, b = self.joints[i]
            start_position = self.vertices[a].position.getTuple()
            end_position = self.vertices[b].position.getTuple()
            pygame.draw.line(screen, self.color, start_position, end_position, self.line_thickness)   
        if self.showPoint == True:
            for vertex in self.vertices:
                vertex.draw(screen)   
        
