from chess import Move
from chess import Board
class Chromosome:
    # Abstract do not initialize
    def __init__(self, body: any):
        self.body = body
        self.score = 0.0
        self.evaluated: bool = False
        self.moves: list[Move] = None
        self.board: str = None

    def set_score(self, score: float) -> None:
        self.score = score

    def set_evaluated(self, evaluated: bool) -> None:
        self.evaluated = evaluated

    def set_moves(self, moves: list[Move]):
        self.moves = moves
        
    def set_board(self, board: str):
        self.board = board

class IntBoard(Chromosome):
    def __init__(self, body: list[int]):
        super().__init__(body)
