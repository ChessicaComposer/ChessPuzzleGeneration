from common.evaluator import EvaluatorResponse
from .base import Fitness

class Utility(Fitness):
    def __init__(self):
        super().__init__()

    def _evaluate_fitness(self, evaluation: EvaluatorResponse) -> float:
        return evaluation.utility
