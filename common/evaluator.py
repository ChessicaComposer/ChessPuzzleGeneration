from chess import Move, Board


class EvaluatorResponse:
    def __init__(self, fen: str, has_mate: bool, utility: float, moves: list[Move]):
        self.fen = fen
        self.has_mate = has_mate
        self.utility = utility
        self.moves = moves

    def print(self):
        print(self.fen)
        print(self.has_mate)
        print(self.utility)
        print(self.moves)


class Evaluator:
    def __init__(self):
        pass

    def run(self, board: Board) -> EvaluatorResponse:
        raise NotImplementedError()
