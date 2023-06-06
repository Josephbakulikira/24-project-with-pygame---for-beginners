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

def RotationX(angle):
    return [
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ]
def RotationY(angle):
    return [
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle), 0, math.cos(angle)]
    ]
def RotationZ(angle):
    return [
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ]

def ProjectionMatrix(z):
    return [
        [z, 0, 0],
        [0, z, 0]
    ]