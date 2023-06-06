import math

def matrix_multiplication(a, b):
    col_a = len(a[0])
    row_a = len(a)
    col_b = len(b[0])
    row_b = len(b)

    result_matrix = [[j for j in range(col_b)] for i in range(row_a)]

    if col_a == row_b:
        for x in range(row_a):
            for y in range(col_b):
                sum = 0
                for k in range(col_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix
    
    else:
        print("Columns of the first matrix must be equal to the rows of the second matrix")
        return None

def Rotation4dXY(angle):
    return [
        [math.cos(angle), -math.sin(angle), 0, 0],
        [math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]
def Rotation4dXZ(angle):
    return [
        [math.cos(angle), 0, -math.sin(angle), 0],
        [0, 1, 0, 0],
        [math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1]]
def Rotation4dXW(angle):
    return [
        [math.cos(angle), 0, 0, -math.sin(angle)],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [math.sin(angle), 0, 0, math.cos(angle)]
        ]
def Rotation4dYZ(angle):
    return [
        [1, 0, 0, 0],
        [0, math.cos(angle), -math.sin(angle), 0],
        [0, math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
        ]
def Rotation4dYW(angle):
    return [
        [1, 0, 0, 0],
        [0, math.cos(angle), 0, -math.sin(angle)],
        [0, 0, 1, 0],
        [0, math.sin(angle), 0, math.cos(angle)]
        ]
def Rotation4dZW(angle):
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, math.cos(angle), -math.sin(angle)],
        [0, 0, math.sin(angle), math.cos(angle)]
        ]

def TesseractRotation():
    return [
        [1, 0, 0],
        [0, math.cos(-math.pi/2), -math.sin(-math.pi/2)],
        [0, math.sin(-math.pi/2), math.cos(-math.pi/2)]
        ]

def ProjectionMatrix(z):
    return [
        [z, 0, 0],
        [0, z, 0]
    ]

def ProjectionMatrix4D(z):
    return [
        [z, 0, 0, 0],
        [0, z, 0, 0],
        [0, 0, z, 0],

    ]