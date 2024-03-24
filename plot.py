import matplotlib.pyplot as plt
import numpy as np

from chromosome import Chromosome
from world import World


def draw_path(world: World, c: Chromosome, name: str) -> None:
    matrix = np.zeros((world.width, world.height))    
    for vec in world.yield_path(c):
        matrix[vec.x, vec.y] += 1
    
    plt.imshow(matrix, cmap="gray")
    plt.plot(world.start.x, world.start.y, "go")
    plt.plot(world.finish.x, world.finish.y, "ro")
    plt.savefig(f"results/{name}.png")
