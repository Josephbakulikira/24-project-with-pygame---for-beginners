from particle import Particle
from vector import Vector
from polygon import Polygon

# BOX SHAPE
def Box(position, length, point_radius=10, thickness=4, color=(255, 123, 150)):
    vertices = [
        Particle(position, point_radius),
        Particle(position + Vector(length, 0), point_radius),
        Particle(position + length, point_radius),
        Particle(position + Vector(0, length), point_radius)
    ]

    joints = [
        [0, 1], [1, 2], [2, 3], [3, 0], [2, 0], [1, 3]
    ]

    return Polygon(vertices, joints, [], thickness, color)

# ROPE SHAPE
def Rope(position, length, n, radius=3, thickness=3, color=(53, 180, 200)):
    x, y = position.getTuple()
    vertices = []
    joints = []
    for i in range(n):
        particle = Particle(Vector(x + length * i, y), radius)
        vertices.append(particle)
    for i in range(n-1):
        joints.append([i, i+1])
    statics = [vertices[0], vertices[-1]]

    return Polygon(vertices, joints, statics, thickness, color)

# CLOTH
def Cloth(position, horiz, vertiz, t, radius=5, thickness=3, vertical=True, horizontal=True, Diagonal1=False, Diagonal2=False, color=(255, 255, 255)):
    x, y = position.getTuple()
    
    # lists
    vertices = []
    joints = []

    for j in range(vertiz):
        for i in range(horiz):
            vertices.append(Particle(Vector(x + i * t, y + j * t), radius))
    
    # HORIZONTAL JOINT
    if horizontal == True:
        for i in range(len(vertices)-1):
            if i % horiz != horiz - 1:
                joints.append([i, i+1])
    # VERTICAL JOINT
    if vertical == True:
        for i in range(len(vertices)-horiz):
            joints.append([i, i+horiz])
    # FIRST DIAGONAL CONNECTION
    if Diagonal1 == True:
        for i in range(len(vertices) - horiz - 1):
            if i % horiz != horiz-1:
                joints.append([i, i+horiz+1])
    # SECOND DIAGONAL CONNECTION
    if Diagonal2 == True:
        for i in range(len(vertices) - horiz):
            if i % horiz != 0:
                joints.append([i, i+horiz-1])
    
    statics = [vertices[0], vertices[horiz//2], vertices[horiz-1]]

    return Polygon(vertices, joints, statics, thickness, color)
    


