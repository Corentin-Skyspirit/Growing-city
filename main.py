import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random

matrix = []
matrix_range = 10

# colors = [
#     # Greens (light → dark)
#     [200/255, 255/255, 200/255, 1.0],
#     [120/255, 200/255, 120/255, 1.0],
#     [60/255, 140/255, 60/255, 1.0],
#     [20/255, 80/255, 20/255, 1.0],

#     # Blues (light → dark)
#     [200/255, 200/255, 255/255, 1.0],
#     [120/255, 120/255, 200/255, 1.0],
#     [60/255, 60/255, 140/255, 1.0],
#     [20/255, 20/255, 80/255, 1.0],

#     # Yellows (light → dark)
#     [255/255, 255/255, 200/255, 1.0],
#     [220/255, 220/255, 120/255, 1.0],
#     [180/255, 180/255, 60/255, 1.0],
#     [120/255, 120/255, 20/255, 1.0],

#     # Purples (light → dark)
#     [240/255, 200/255, 255/255, 1.0],
#     [180/255, 120/255, 220/255, 1.0],
#     [120/255, 60/255, 160/255, 1.0],
#     [60/255, 20/255, 100/255, 1.0],
# ]

colors = [
    [0.9, 0.9, 0.9, 1.],
    [0.3, 0.3, 0.3, 1.],
    [120/255, 200/255, 120/255, 1.0],
    [120/255, 120/255, 200/255, 1.0],
]
new_cmap = mcolors.ListedColormap(colors) 

for _ in range(matrix_range):
    line = []
    for _ in range(matrix_range):
        line.append(0)
    matrix.append(line)

matrix[4][4] = 2

def getNeighbor(i:int, j:int) -> list:
    neighbor = []
    
    if i > 0: neighbor.append(matrix[i-1][j])
    if j > 0: neighbor.append(matrix[i][j-1])

    if i < matrix_range-1: neighbor.append(matrix[i+1][j])
    if j < matrix_range-1: neighbor.append(matrix[i][j+1])

    if i > 0 and j > 0: neighbor.append(matrix[i-1][j-1])
    if i > 0 and j < matrix_range-1: neighbor.append(matrix[i-1][j+1])

    if i < matrix_range-1 and j > 0: neighbor.append(matrix[i+1][j-1])
    if i < matrix_range-1 and j < matrix_range-1: neighbor.append(matrix[i+1][j+1])
    return neighbor

def chanceOfBuilding(i:int, j:int) -> int:
    neighbor = getNeighbor(i, j)
    prob = random.randint(0, 100)
    if neighbor.count(2) == 0: return prob / 2

    if neighbor.count(2) == 8: return prob * 3
    elif neighbor.count(2) > 5: return prob * 2
    elif neighbor.count(2) > 3: return prob * 1.5
    else: return prob

def houseLevel(h:int, s:int):
    
    return

def shopLevel(h:int, s:int):

    return

def compute():
    for i in range(matrix_range):
        for j in range(matrix_range):
            value = matrix[i][j]
            prob = chanceOfBuilding(i, j)
            if value == 2:
                prob *= 2
            if prob > 70: value = 2
            else: value = 0
            matrix[i][j] = value

def roadGeneration():
    return

def display():
    cax = plt.imshow(matrix, cmap=new_cmap, interpolation="nearest", aspect='auto')
    plt.xticks([])
    plt.yticks([])

def run(i):
    compute()
    display()

if __name__ == '__main__' :
    ani = FuncAnimation(plt.gcf(), run, interval=1000)
    plt.tight_layout()
    plt.show()