import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import copy

matrix_range = 100

empty = 0
road = 1
house = 2
shop = 3

colors = [
    [0.9, 0.9, 0.9, 1.],
    [0.3, 0.3, 0.3, 1.],
    [120/255, 200/255, 120/255, 1.0],
    [120/255, 120/255, 200/255, 1.0],
]

def setup() -> list:
    matrix = []

    for _ in range(matrix_range):
        line = []
        for _ in range(matrix_range):
            line.append(empty)
        matrix.append(line)

    matrix[matrix_range//2][matrix_range//2] = house
    matrix[matrix_range//2+1][matrix_range//2+1] = house
    
    return matrix

fig, ax = plt.subplots(figsize=(7, 7))
plt.tight_layout(pad=3.5)
new_cmap = mcolors.ListedColormap(colors)
cax = ax.imshow(setup(), cmap=new_cmap, interpolation="nearest", aspect='auto', vmin=0, vmax=len(colors))
fig.colorbar(cax, fraction=0.03, pad=0.04)

def getNeighbor(i:int, j:int, matrix) -> list:
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

def chanceOfBuilding(i:int, j:int, matrix:list) -> int:
    neighbor = getNeighbor(i, j, matrix)
    prob = random.randint(0,500)
    prob += (neighbor.count(house) * 1000)
    if neighbor.count(house) > 3: prob += 1000
    prob += (neighbor.count(shop) * 1500)
    return prob

def houseLevel(h:int, s:int):
    
    return

def shopLevel(h:int, s:int):

    return

def compute():
    global matrix
    global old_matrix
    for i in range(matrix_range):
        for j in range(matrix_range):

            value = old_matrix[i][j]
            prob = chanceOfBuilding(i, j, old_matrix)

            if value != empty: prob += 1400

            if prob < 1500: value = empty
            elif prob > 2000:
                shopNumber = getNeighbor(i, j, old_matrix).count(shop)
                shopProb = 0
                if shopNumber > 2:
                    shopProb = 30
                elif shopNumber < 6:
                    shopProb = 10
                elif shopNumber < 3:
                    shopProb = 50
                if value == shop: shopProb += 40
                if random.randint(0,100) < shopProb: value = shop
                else: value = house
                if random.randint(0,100) < 30:
                    value = empty
            
            matrix[i][j] = value
    old_matrix = copy.deepcopy(matrix)

def roadGeneration():
    return

def display(matrix):
    cax = ax.imshow(matrix, cmap=new_cmap, interpolation="nearest", aspect='auto', vmin=0, vmax=len(colors))
    ax.set_xticks([])
    ax.set_yticks([])

def run(i):
    global matrix
    global old_matrix
    if i == 0:
        matrix = setup()
        old_matrix = copy.deepcopy(matrix)
    compute()
    display(matrix)

if __name__ == '__main__' :

    ani = FuncAnimation(plt.gcf(), run, interval=2000)
    plt.tight_layout()
    plt.show()