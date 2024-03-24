from math import sqrt, pow
from typing import List
from random import randint, choice

from chromosome import Chromosome
from vector2d import Vector2D
from action import Action


class World:
    __width: int
    __height: int
    __start: Vector2D
    __finish: Vector2D

    def __init__(self, width: int, height: int, start: Vector2D, finish: Vector2D) -> None:
        self.__width = width
        self.__height = height
        self.__start = start
        self.__finish = finish

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def start(self) -> Vector2D:
        return self.__start

    @property
    def finish(self) -> Vector2D:
        return self.__finish
    
    def yield_path(self, c: Chromosome):
        pos = Vector2D(self.__start.x, self.__start.y)
        for action in c.steps:
            if action == Action.LEFT and pos.x > 0:
                pos.set_x(pos.x - 1)
                yield pos
            elif action == Action.UP and pos.y > 0:
                pos.set_y(pos.y - 1)
                yield pos
            elif action == Action.RIGHT and pos.x < self.__width - 2:
                pos.set_x(pos.x + 1)
                yield pos
            elif action == Action.DOWN and pos.x < self.__height - 2:
                pos.set_y(pos.y + 1)
                yield pos
    
    def __exec_chromosome(self, c: Chromosome) -> Vector2D:
        pos = Vector2D(self.__start.x, self.__start.y)
        for action in c.steps:
            if action == Action.LEFT and pos.x > 0:
                pos.set_x(pos.x - 1)
            elif action == Action.UP and pos.y > 0:
                pos.set_y(pos.y - 1)
            elif action == Action.RIGHT and pos.x < self.__width - 2:
                pos.set_x(pos.x + 1)
            elif action == Action.DOWN and pos.x < self.__height - 2:
                pos.set_y(pos.y + 1)
        return pos

    def evaluate_chromosome(self, c: Chromosome) -> float:
        """
        Evaluating a chromosome. Less score is better
        """
        DISTANCE_WEIGHT         = 0.8
        STEPS_LENGTH_WEIGHT     = 0.2

        state = self.__exec_chromosome(c)
        distance = sqrt(pow(state.x - self.__finish.x, 2) + pow(state.y - self.__finish.y, 2))
        score = distance * DISTANCE_WEIGHT + len(c.steps) * STEPS_LENGTH_WEIGHT
        return score

    def cross_over(self, c1: Chromosome, c2: Chromosome) -> List[Chromosome]:
        size = min(len(c1.steps), len(c2.steps))
        cxpoint1 = randint(0, size)
        cxpoint2 = randint(0, size - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1
        
        offspring1 = Chromosome(genes=c1.steps[:cxpoint1] + c2.steps[cxpoint1: cxpoint2] + c1.steps[cxpoint2:])
        offspring2 = Chromosome(genes=c2.steps[:cxpoint1] + c1.steps[cxpoint1: cxpoint2] + c2.steps[cxpoint2:])
        return [offspring1, offspring2]

    def mutate(self, c: Chromosome) -> None:
        MUTATIONS = ["RANDOM", "SWAP", "INVERSION", "ADDITION", "DELETION"]
        selected_mutation = choice(MUTATIONS)
        
        if len(c.steps) < 3:
            return

        if selected_mutation == "RANDOM":
            n = randint(0, len(c.steps) - 1)
            for _ in range(0, n):
                c.steps[randint(0, len(c.steps) - 1)] = Action(randint(0, 3))
        elif selected_mutation == "SWAP":
            g1 = randint(0, len(c.steps) - 1)
            g2 = randint(0, len(c.steps) - 1)
            c.steps[g1], c.steps[g2] = c.steps[g2], c.steps[g1]
        elif selected_mutation == "INVERSION":
            if len(c.steps) < 2:
                return
            i1 = randint(0, len(c.steps) - 2)
            i2 = randint(i1 + 1, len(c.steps) - 1)

            sub_gene = c.steps[i1:i2 + 1]
            inverted = sub_gene[::-1]

            c.steps[i1: i2+1] = inverted
        elif selected_mutation == "ADDITION":
            c.steps.insert(randint(0, len(c.steps) - 1), Action(randint(0, 3)))
        elif selected_mutation == "DELETION":
            c.steps.pop(randint(0, len(c.steps) - 1))
    
    def is_winner(self, c: Chromosome) -> bool:
        state = self.__exec_chromosome(c)
        return abs(state.x - self.__finish.x) <= 1 and abs(state.y - self.__finish.y) <= 1
