from base import Tournament
from ..chromosome import IntBoard

class SortedAscending(Tournament):
    def run(self, population: list[IntBoard]) -> list[IntBoard]:
        population.sort(key=lambda c: c.score)
        print(list(map(lambda c: c.score, population)))
        population = population[len(population) // 2:]
        return population