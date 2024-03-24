from typing import List
from random import randrange

from action import Action


class Chromosome:
    __steps: List[Action]

    def __init__(self, genes: List[Action] = []) -> None:
        self.__steps = []
        if len(genes) == 0:
            for i in range(2, randrange(5, 100)):
                self.__steps.append(Action(randrange(0, 4)))
        else:
            self.__steps = genes
    
    @property
    def steps(self) -> List[Action]:
        return self.__steps

    def __str__(self) -> str:
        return str(self.__steps)
    
    def __repr__(self) -> str:
        return str(self.__steps)
