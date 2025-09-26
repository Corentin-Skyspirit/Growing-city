import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import copy

matrix_range = 50

empty = 0
road = 1
house = 2
house2 = 3
shop = 4
shop2 = 5

colors = [
    [0.9, 0.9, 0.9, 1.],
    [0.3, 0.3, 0.3, 1.],
    [120/255, 200/255, 120/255, 1.0],
    [60/255, 140/255, 60/255, 1.0],
    [120/255, 120/255, 200/255, 1.0],
    [60/255, 60/255, 140/255, 1.0],
]

def setup() -> list:
    matrix = []

    for _ in range(matrix_range):
        line = []
        for _ in range(matrix_range):
            line.append(empty)
        matrix.append(line)
    
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
    nearHouseCount = nearNeighbor.count(house) + nearNeighbor.count(house2)
    nearShopCount = nearNeighbor.count(shop) + nearNeighbor.count(shop2)
    prob = 0

    if actualBuild == house: 
        prob = 70
        prob += nearHouseCount * 2.5
        prob += nearShopCount * 5
        prob += (neighbor.count(shop) * 2) + (neighbor.count(shop2) * 3) - nearShopCount
        prob += neighbor.count(house) + (neighbor.count(house2) * 1.5) - nearHouseCount
        prob += neighbor.count(empty) - nearNeighbor.count(empty)
        if (nearShopCount > 0 and nearHouseCount > 4) :
            prob += 20

    elif actualBuild == shop: 
        prob = 60
        prob += nearHouseCount * 3
        prob += nearShopCount * 3
        prob += (neighbor.count(house) * 2) + (neighbor.count(house2) * 3) - nearHouseCount
        prob -= neighbor.count(shop) + (neighbor.count(shop2) * 1.5) - nearShopCount
        prob -= neighbor.count(empty)
        if (nearShopCount < 2 and neighbor.count(house) + (neighbor.count(house2) * 1.5) > 7) :
            prob += 30

    else: 
        prob += nearHouseCount * 3
        prob += nearShopCount * 4.5
        prob += (neighbor.count(shop) * 2)+ (neighbor.count(shop2) * 2.5) - nearShopCount
        prob += (neighbor.count(house) * 1.5) + (neighbor.count(house) * 2) - nearHouseCount
        prob += neighbor.count(empty) - nearNeighbor.count(empty)
        if (nearShopCount > 0 and nearHouseCount > 2) :
            prob += 20

    if neighbor.count(empty) <= 10:
        prob += 20

    return prob

def newBuildingType(i:int, j:int, actualBuild:int, neighbor:list, nearNeighbor:list):
    buildingType = empty
    houseChance = 0
    shopChance = 0
    if actualBuild == house: houseChance += 15
    elif actualBuild == shop: shopChance += 15

    houseChance += neighbor.count(shop) + neighbor.count(shop2) * 1.5
    houseChance += (int)(neighbor.count(empty)/1)
    if nearNeighbor.count(shop) + nearNeighbor.count(shop2) > 5:
        houseChance -= 10

    nearShopCount = nearNeighbor.count(shop) + nearNeighbor.count(shop2) * 1.5
    shopChance += neighbor.count(house) + neighbor.count(house2)
    # shopChance += nearShopCount 
    # shopChance -= neighbor.count(shop) + neighbor.count(shop2) * 1.5 - nearShopCount
    shopChance += neighbor.count(shop) + neighbor.count(shop2) * 1.5

    if houseChance + shopChance < 3:
        return empty
    if houseChance < shopChance:
        buildingType = shop
    else:
        buildingType = house
    # print(actualBuild, " - shop:", shopChance, "/ house:", houseChance)
    return buildingType

def houseLevel(h:int, s:int):
    
    return

def shopLevel(h:int, s:int):

    return

def newBuilding(i:int, j:int, matrix:list) -> int:
    oldBuilding = matrix[i][j]
    building = empty
    neighbor = getNeighbor(i, j, matrix)
    if neighbor.count(empty) == 21 : return empty
    else:
        nearNeighbor = getNearNeighbor(i, j, matrix)
        prob = chanceOfBuilding(i, j, oldBuilding, neighbor, nearNeighbor)
        if prob < 0: return empty
        if prob >= 100:
            if oldBuilding == house: return house2
            elif oldBuilding == shop: return shop2
        else:
            building = newBuildingType(i, j, oldBuilding, neighbor, nearNeighbor)
        if prob < 100:
            if random.randint(0,100) > prob: building = empty
        
        # print("[", i*matrix_range + j, "] builds: ", oldBuilding, " / ", building, "prob:", prob, "neighbor:", neighbor.count(empty))
    return building

def compute():
    global matrix
    global old_matrix
    for i in range(2, matrix_range-2):
        for j in range(2, matrix_range-2):

            value = newBuilding(i, j, old_matrix)
            
            matrix[i][j] = value
    old_matrix = copy.deepcopy(matrix)

def roadGeneration(matrix):
    return

def riverGeneration(matrix):
    return

def cityGeneration(matrix):
    for i in range(0, 4):
        for j in range(0, 4):
            res = random.randint(0, 10)
            if res > 3:
                matrix[(matrix_range+i)//2][(matrix_range+j)//2] = ((res%2 + 1) * 2)
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
    elif i == 1:
        riverGeneration(matrix)
        roadGeneration(matrix)
        cityGeneration(matrix)
        old_matrix = copy.deepcopy(matrix)
    else:
        compute()
    display(matrix)

if __name__ == '__main__' :

    ani = FuncAnimation(plt.gcf(), run, interval=1000)
    plt.tight_layout()
    plt.show()