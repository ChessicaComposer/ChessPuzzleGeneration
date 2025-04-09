from genetic.crossover.base import Crossover
from genetic.mutation.mutation import Mutation
from .fitness import Fitness
from .genetic import Genetic
from common.evaluator import Evaluator
from .chromosome import IntBoard

class FullBoard(Genetic):
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None,
                 fitness: Fitness = None, max_fitness: float = 10.0):
        super().__init__(evaluator, crossover, mutation, fitness, max_fitness)

    # Create population

    def _run_tournament(self, population: list[IntBoard]) -> list[IntBoard]:
        population.sort(key=lambda c: c.score)
        print(list(map(lambda c: c.score, population)))
        population = population[len(population) // 2:]
        return population

    def _stop_condition(self, generation) -> bool:
        return False
