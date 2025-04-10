from chess_engine import ChessEngine
from .crossover.singlepoint import SinglePoint
from .fitness.checkmate import Checkmate
from .genetic import Genetic
from .mutation.add_random_pieces import AddRandomPieces
from .population.kings_court import KingsCourt
from .tournament.sorted_ascending import SortedAscending


class Composer(Genetic):
    def __init__(self, cutoff = 5):
        super().__init__(
            evaluator = ChessEngine(cutoff),
            crossover = SinglePoint(),
            mutation = AddRandomPieces(),
            fitness = Checkmate(),
            population = KingsCourt(),
            tournament = SortedAscending(),
            max_fitness = 10.0
        )

    def _stop_condition(self, generation) -> bool:
        return False
