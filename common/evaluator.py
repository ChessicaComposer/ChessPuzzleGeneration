import chess


class EvaluatorResponse:
    def __init__(self, has_mate: bool, utility: float, moves: list[chess.Move], fen: str):
        self.has_mate = has_mate
        self.utility = utility
        self.moves = moves
        self.fen = fen

class Evaluator:
    def __init__(self):
        pass

    def run(self, board: chess.Board) -> EvaluatorResponse:
        raise NotImplementedError()
