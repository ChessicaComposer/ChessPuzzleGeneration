from genetic.crossover.base import Crossover
from genetic.mutation.mutation import Mutation
from .fitness import Fitness
from .genetic import Genetic
from common.evaluator import Evaluator

class Composer(Genetic):
    def __init__(self, evaluator: Evaluator = None, crossover: Crossover = None, mutation: Mutation = None,
                 fitness: Fitness = None, max_fitness: float = 10.0):
        super().__init__(evaluator, crossover, mutation, fitness, max_fitness)

    def _stop_condition(self, generation) -> bool:
        return False
