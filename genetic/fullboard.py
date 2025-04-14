from chess_engine import ChessEngine
from genetic.crossover.pv_line import PvLine
from genetic.tournament.sorted_ascending import SortedAscending
from .crossover.singlepoint import SinglePoint
from .crossover.twopoint import TwoPoint
from .fitness.checkmate import Checkmate
from .genetic import Genetic
from .mutation.random_forward_moves import RandomForwardMoves
from .population.random_moves import RandomMoves

class FullBoard(Genetic):
    def __init__(self, cutoff = 5):
        super().__init__(
            evaluator = ChessEngine(cutoff),
            crossover = PvLine(),
            mutation = RandomForwardMoves(),
            fitness = Checkmate(),
            population = RandomMoves(),
            tournament = SortedAscending(),
            max_fitness = 10.0
        )