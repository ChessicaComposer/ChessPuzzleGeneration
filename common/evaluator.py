import chess

class EvaluatorResponse:
    def __init__(self, fen: str, has_mate: bool, utility: float, moves):
        self.fen = fen
        self.has_mate = has_mate
        self.utility = utility
        self.moves = moves


class Evaluator:
    def __init__(self):
        pass

    def run(self, board: chess.Board) -> EvaluatorResponse:
        raise NotImplementedError()
