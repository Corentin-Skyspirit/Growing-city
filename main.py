import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random

matrix = []
matrix_range = 10

for _ in range(matrix_range):
    line = []
    for _ in range(matrix_range):
        line.append(0)
    matrix.append(line)

def compute():
    for i in range(matrix_range):
        line = []
        for _ in range(matrix_range):
            line.append(random.randint(0, 5))
        matrix[i] = line

def display():
    colors = plt.cm.viridis(np.linspace(0, 1, 256))
    colors[0] = [0.3, 0.3, 0.3, 1]
    new_cmap = mcolors.ListedColormap(colors)
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