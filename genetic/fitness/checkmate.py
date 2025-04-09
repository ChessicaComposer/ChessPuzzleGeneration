from common.evaluator import EvaluatorResponse
from .base import Fitness

class Checkmate(Fitness):
    def __init__(self):
        super().__init__()

    def _evaluate_fitness(self, evaluation: EvaluatorResponse) -> float:
        if evaluation.has_mate:
            return 10
        return 0