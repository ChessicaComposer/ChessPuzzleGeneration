import chess


class EvaluatorResponse:
    def __init__(self, has_mate: bool, utility: float):
        self.has_mate = has_mate
        self.utility = utility


class Evaluator:
    def __init__(self):
        pass

    def run(self, board: chess.Board) -> EvaluatorResponse:
        raise NotImplementedError()
