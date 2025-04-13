import chess

from common.evaluator import EvaluatorResponse
from feature_detector.feature_detector import FeatureDetector
from .base import Fitness


class Handmaiden(Fitness):
    def __init__(self):
        super().__init__()
        self.fd = FeatureDetector()

    def _evaluate_fitness(self, evaluation: EvaluatorResponse) -> float:
        res = 0
        if not evaluation.has_mate:
            return res

        feats = self.fd.run(evaluation)

        if len(evaluation.moves.line) > 1:      res += 1
        if len(feats.king_attackers) > 1:          res += 10
        if feats.king_attackers.__contains__(chess.QUEEN):   res += 10; print("- White Queen checkmates!")
        if len(feats.checkers) > 1:             res += 10; print("- Multi-checkers!");
        if evaluation.utility > 0:              res += 1;
        return res
