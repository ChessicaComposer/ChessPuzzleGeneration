class EvaluatorResponse:
    def __init__(self, has_mate: bool):
        self.has_mate = has_mate

class Evaluator:
    def __init__(self):
        pass

    def run() -> EvaluatorResponse:
        raise NotImplementedError()