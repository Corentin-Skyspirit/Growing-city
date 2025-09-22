import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
import numpy as np
import random

matrix = []
matrix_range = 10

colors = [
    # green (light → dark)
    (200, 255, 200, 255),
    (120, 200, 120, 255),
    (60, 140, 60, 255),
    (20, 80, 20, 255),

    # blue (light → dark)
    (200, 200, 255, 255),
    (120, 120, 200, 255),
    (60, 60, 140, 255),
    (20, 20, 80, 255),

    # yellow (light → dark)
    (255, 255, 200, 255),
    (220, 220, 120, 255),
    (180, 180, 60, 255),
    (120, 120, 20, 255),

    # purple (light → dark)
    (240, 200, 255, 255),
    (180, 120, 220, 255),
    (120, 60, 160, 255),
    (60, 20, 100, 255),
]
new_cmap = mcolors.ListedColormap(colors) 

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