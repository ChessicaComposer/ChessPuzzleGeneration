import chess


class EvaluatorResponse:
    def __init__(self, has_mate: bool, score: int = 0):
        self.has_mate = has_mate
        self.score = score


class Evaluator:
    def __init__(self):
        pass

    def run(self, board: chess.Board) -> EvaluatorResponse:
        raise NotImplementedError()
