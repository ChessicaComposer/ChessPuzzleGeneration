import chess


class EvaluatorResponse:
    def __init__(self, has_mate: bool):
        self.has_mate = has_mate


class Evaluator:
    def __init__(self):
        pass

    def run(self, board: chess.Board) -> EvaluatorResponse:
        raise NotImplementedError()
