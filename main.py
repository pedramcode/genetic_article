from random import randint, random

from world import World
from vector2d import Vector2D
from chromosome import Chromosome
from plot import draw_path


def main():
    world = World(50, 50, Vector2D(0, 0), Vector2D(49, 49))
    population = [Chromosome() for _ in range(0, 10)]

    i = 0
    for c in population:
        draw_path(world, c, f"chromosome_{i}")
        i += 1

    for generation in range(0, 100000):
        population = sorted(population, key=world.evaluate_chromosome)[:int(len(population) / 3)]

        if world.is_winner(population[0]):
            print(f"Path found at generation: {generation}")
            print(f"Score: ", world.evaluate_chromosome(population[0]))
            draw_path(world, population[0], "result")
            return

        children = world.cross_over(population[0], population[1])

        for i in range(0, randint(1, 10)):
            [c1, c2] = world.cross_over(population[randint(0, len(population) - 1)], population[randint(0, len(population) - 1)])
            children.extend([c1, c2])

        for c in children:
            if random() < 0.3:
                world.mutate(c)

        population.extend(children)

if __name__ == "__main__":
    main()
