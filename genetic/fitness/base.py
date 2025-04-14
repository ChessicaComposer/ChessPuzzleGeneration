from common import Evaluator, EvaluatorResponse
from ..chromosome import Chromosome
from ..utility import chess_int_to_board


class Fitness(Evaluator):
    def __init__(self):
        super().__init__()
        self.evaluator = None

    def score(self, chromosome: Chromosome) -> Chromosome:
        if chromosome.evaluated:
            return chromosome
        board = chess_int_to_board(chromosome.body)
        chromosome.set_evaluated(True)
        if not board.is_valid():
            chromosome.set_score(-10)
            return chromosome

        evaluation: EvaluatorResponse = self.evaluator.run(board)
        fitness = self._evaluate_fitness(evaluation)
        chromosome.set_score(fitness)
        # Save moves and board in chromosome (used for pv-line crossover)
        chromosome.set_moves(evaluation.moves)
        chromosome.set_board(evaluation.fen)

        return chromosome

    def _evaluate_fitness(self, evaluation: EvaluatorResponse) -> float:
        raise NotImplementedError()

    def set_evaluator(self, evaluator: Evaluator):
        self.evaluator = evaluator