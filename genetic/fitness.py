from common import Evaluator
from .chromosome import Chromosome

class Fitness(Evaluator):
    def __init__(self):
        super().__init__()
        self.evaluator = None

    def score(self, population: Chromosome) -> Chromosome:
        raise NotImplementedError()

    def set_evaluator(self, evaluator: Evaluator):
        self.evaluator = evaluator