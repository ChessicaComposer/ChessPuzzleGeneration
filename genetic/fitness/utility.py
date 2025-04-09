from common.evaluator import EvaluatorResponse
from base import Fitness
from ..utility import chess_board_to_int, chess_int_to_board
from .. chromosome import IntBoard

class Utility(Fitness):
    def __init__(self):
        super().__init__()

    def score(self, chromosome: IntBoard) -> IntBoard:
        if chromosome.evaluated:
            return chromosome
        board = chess_int_to_board(chromosome.body)
        chromosome.set_evaluated(True)
        if not board.is_valid():
            chromosome.set_score(-10)
            return chromosome
        evaluation: EvaluatorResponse = self.evaluator.run(board)
        chromosome.set_score(evaluation.utility)
        return chromosome
