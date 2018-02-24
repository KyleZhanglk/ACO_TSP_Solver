"""read tsp file"""
import math
import random


def euc_2d(a, b):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))


def load_data(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        while not line.startswith('NODE_COORD_SECTION'):
            line = f.readline()
        
        points = []
        line = f.readline()
        while not line.startswith('EOF'):
            line = line.split(' ')
            points.append((float(line[1]), float(line[2])))
            line = f.readline()

    n = len(points)
    result = []
    for i in range(n):
        result.append([0] * n)
    for i in range(n - 1):
        for j in range(i + 1, n):
            result[i][j] = euc_2d(points[i], points[j])
            result[j][i] = result[i][j]
    return result