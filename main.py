import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import copy

matrix_range = 10

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

def getNearNeighbor(i:int, j:int, matrix) -> list:
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

def getNeighbor(i:int, j:int, matrix) -> list:
    neighbor = []

    neighbor += matrix[i-2][j-1:j+2]
    neighbor += matrix[i-1][j-2:j+3]
    neighbor += matrix[i][j-2:j+3]
    neighbor += matrix[i+1][j-2:j+3]
    neighbor += matrix[i+2][j-1:j+2]

    return neighbor

def chanceOfBuilding(i:int, j:int, actualBuild: int, neighbor:list, nearNeighbor:list) -> int:
    if actualBuild != empty: prob = 50 
    else: prob = 0
    
    nearHouseCount = nearNeighbor.count(house)
    nearShopCount = nearNeighbor.count(shop)
    prob += nearHouseCount * 2
    prob += nearShopCount * 4
    prob += neighbor.count(house) - nearHouseCount
    prob += (neighbor.count(shop) *2) - nearShopCount

    return prob

def newBuildingType(i:int, j:int, actualBuild:int, neighbor:list, nearNeighbor:list):
    buildingType = empty
    houseChance = 0
    shopChance = 0
    if actualBuild == house: houseChance += 10
    elif actualBuild == shop: shopChance += 10

    houseChance += neighbor.count(shop)
    houseChance += neighbor.count(empty)

    nearShopCount = nearNeighbor.count(shop)
    shopChance += neighbor.count(house)
    shopChance += nearShopCount
    shopChance -= neighbor.count(shop) - nearShopCount

    if houseChance < shopChance:
        buildingType = shop
    else:
        buildingType = house
    return buildingType

def houseLevel(h:int, s:int):
    
    return

def shopLevel(h:int, s:int):

    return

def newBuilding(i:int, j:int, matrix:list) -> int:
    oldBuilding = matrix[i][j]
    neighbor = getNeighbor(i, j, matrix)
    if neighbor.count(empty) == 21 : return empty
    else:
        nearNeighbor = getNearNeighbor(i, j, matrix)
        prob = chanceOfBuilding(i, j, oldBuilding, neighbor, nearNeighbor)
        if prob > 100: print("oui")
        building = newBuildingType(i, j, oldBuilding, neighbor, nearNeighbor)
        if prob < 100:
            if random.randint(0,100) < prob: building = empty
        
        print("[", i*matrix_range + j, "] builds: ", oldBuilding, " / ", building, "prob:", prob)

    return building

def compute():
    global matrix
    global old_matrix
    for i in range(2, matrix_range-2):
        for j in range(2, matrix_range-2):

            value = newBuilding(i, j, old_matrix)
            
            matrix[i][j] = value
    old_matrix = copy.deepcopy(matrix)

def roadGeneration():
    return

def riverGeneration():
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