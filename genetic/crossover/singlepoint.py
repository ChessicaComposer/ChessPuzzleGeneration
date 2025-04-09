from genetic.crossover.base import Crossover
from .. chromosome import IntBoard

class SinglePoint(Crossover):
    def __init__(self):
        super().__init__()

    def _mate(self, parent1: IntBoard, parent2: IntBoard) -> list[IntBoard]:
        half = len(parent1.body) // 2
        return [IntBoard(parent1.body[:half] + parent2.body[half:]),
                IntBoard(parent2.body[:half] + parent1.body[half:])]

    def reproduce(self, population: list[IntBoard]) -> list[IntBoard]:
        offspring: list[IntBoard] = []
        for i in range(0, len(population) - 1, 2):
            children = self._mate(population[i], population[i + 1])
            offspring += children
        if len(population) % 2 != 0:
            children = self._mate(population[0], population[-1])
            offspring.append(children[0])
        return offspring