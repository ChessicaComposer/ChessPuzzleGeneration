from chess_engine import ChessEngine
from .crossover.singlepoint import SinglePoint
from .fitness.checkmate import Checkmate
from .genetic import Genetic
from .mutation.random_forward_moves import RandomForwardMoves
from .population.random_moves import RandomMoves

class FullBoard(Genetic):
    def __init__(self, cutoff = 5):
        super().__init__(
            evaluator = ChessEngine(cutoff),
            crossover = SinglePoint(),
            mutation = RandomForwardMoves(),
            fitness = Checkmate(),
            population = RandomMoves(),
            max_fitness = 10.0
        )